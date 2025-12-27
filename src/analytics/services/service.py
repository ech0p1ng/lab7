import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    balanced_accuracy_score,
    f1_score,
    confusion_matrix,
    roc_curve,
    auc
)
import matplotlib.pyplot as plt
from sklearn.base import ClassifierMixin, RegressorMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from logger import logger
from storage.services.minio_service import MinioService
from typing import Any


class AnalyticsService:
    def __init__(self, minio_service: MinioService) -> None:
        self.minio_service = minio_service

    def __save_csv(self, df: pd.DataFrame, path: str) -> None:
        csv_save_kwargs = {
            'sep': ';',
            'encoding': 'utf-8',
            'index': False,
        }

        return df.to_csv(path, **csv_save_kwargs)  # type: ignore

    async def __load_csv(self, url: str) -> pd.DataFrame:
        file_name = url.split('/')[-1]
        file_url = self.minio_service.get_file_url(file_name)
        await self.minio_service.download_file(
            url=file_url,
            filename=file_name
        )

        csv_load_kwargs = {
            'sep': ';',
            'encoding': 'utf-8',
        }

        return pd.read_csv(url, **csv_load_kwargs)  # type: ignore

    def _train_test_split(self, df: pd.DataFrame) -> list:
        X = df.drop(columns=['relevance'])
        # y = df['relevance']
        y = (df['relevance'] > df['relevance'].median()).astype(int)  # 0 или 1 (нерелевантно/релевантно)

        return train_test_split(
            X, y,
            test_size=0.2,
            random_state=42     # Для воспроизводимости результатов
        )

    def apply_model(
        self,
        model: ClassifierMixin | RegressorMixin,
        x_train: np.ndarray,
        x_test: np.ndarray,
        y_train: np.ndarray
    ) -> np.ndarray:
        _x_train = x_train
        _x_test = x_test

        if isinstance(model, KNeighborsClassifier):
            scaler = StandardScaler()
            _x_train = scaler.fit_transform(x_train)
            _x_test = scaler.transform(x_test)

        model.fit(_x_train, y_train)  # type: ignore
        return model.predict(_x_test)  # type: ignore

    def calc_scores(
        self,
        y_test: np.ndarray,
        y_pred: np.ndarray
    ) -> dict[str, float]:
        _average = 'binary' if len(np.unique(y_test)) == 2 else 'weighted'
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average=_average)
        recall = recall_score(y_test, y_pred, average=_average)
        balanced_accuracy = balanced_accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average=_average)
        return {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'balanced_accuracy': float(balanced_accuracy),
            'f1': float(f1),
        }

    def _confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> pd.DataFrame:
        cm = confusion_matrix(y_true, y_pred)
        confusion_matrix_df = pd.DataFrame(
            cm,
            index=['Настоящее 0', 'Настоящее 1'],
            columns=['Предсказанное 0', 'Предсказанное 1']
        )
        return pd.DataFrame(confusion_matrix_df)

    def _roc_curve(
        self,
        y_test: np.ndarray,
        y_pred: np.ndarray,
        model_name: str
    ) -> tuple:
        fpr, tpr, _ = roc_curve(y_test, y_pred)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr)
        plt.title(f'{model_name} (AUC = {roc_auc:.4f})')
        plt.show()
        return (fpr, tpr, roc_auc, model_name)

    async def analyze(self) -> dict[str, Any]:
        file_name = 'temp/train_data_fixed.csv'

        df = await self.__load_csv(file_name)
        X_train, X_test, y_train, y_test = self._train_test_split(df)

        models = [
            KNeighborsClassifier(n_neighbors=5),
            LogisticRegression(max_iter=1000, random_state=42),
            RandomForestClassifier(
                n_estimators=100,  # количество деревьев
                random_state=42,  # для воспроизводимости
                n_jobs=-1  # использовать все ядра процессора
            )
        ]

        scores = []
        confusion_matrixes: list[pd.DataFrame] = []
        roc_data = []
        for model in models:
            predicted = self.apply_model(model, X_train, X_test, y_train)  # type: ignore
            model_name = type(model).__name__
            self._roc_curve(y_test, predicted, model_name)
            scores.append({
                **self.calc_scores(y_test, predicted),
                'model': model_name
            })

            confusion_matrixes.append(self._confusion_matrix(y_test, predicted))

        results = []

        for i, c in enumerate(confusion_matrixes):
            results.append({
                'method': type(models[i]).__name__,
                'matrix': c.to_dict()
            })
        return {
            'table': {
                'name': 'Оценка ошибки классификации',
                'data': pd.DataFrame(scores).to_dict()
            },
            'confussion_matrixes': results
        }
