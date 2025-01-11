import json
from decimal import Decimal
from datetime import datetime
from typing import Any, Dict, List, Type


class BaseSerializer(json.JSONEncoder):
    model: Type = None  # Clase del modelo (opcional)
    fields: List[str] = None  # Lista de campos a serializar

    def __init__(self, *args, **kwargs):
        # Permitir inicializar con campos personalizados
        self.fields = kwargs.pop("fields", self.fields)
        super().__init__(*args, **kwargs)

    def default(self, obj: Any) -> Any:
        # Convertir Decimal a float
        if isinstance(obj, Decimal):
            return float(obj)

        # Convertir datetime a string
        if isinstance(obj, datetime):
            return obj.isoformat()

        # Si se proporciona un modelo y los campos están definidos
        if self.model:
            return self._serialize_model(obj)

        # Si el objeto es de otro tipo, intentar usar la implementación por defecto
        return super().default(obj)

    def _serialize_model(self, obj: Any) -> Dict[str, Any]:
        """Serializa un objeto de modelo respetando los campos definidos."""
        if not self.fields:
            raise ValueError("Debe definir los campos a serializar.")

        serialized_data = {}
        for field in self.fields:
            value = getattr(obj, field)
            # Procesar tipos específicos durante la serialización
            if isinstance(value, Decimal):
                value = float(value)
            elif isinstance(value, datetime):
                value = value.isoformat()
            serialized_data[field] = value

        return serialized_data

    @classmethod
    def serialize_data(cls, data: Any, **kwargs) -> str:
        """Serializa los datos utilizando el BaseSerializer."""
        if cls.model:
            return cls(**kwargs).default(data)
