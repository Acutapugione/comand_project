from pydantic import BaseModel
from sqlalchemy import MetaData
from functools import wraps


def generate_pydantic_models(meta: MetaData, base_postfix: str = "Base", create_postfix: str = "Create", full_postfix: str = "", base_model_exclude_columns: [] = []) -> [type]:
    "Function to generate Pydantic models from SQLAlchemy metadata"
    pydantic_models = []

    for name, model in meta.tables.items():
        # parse columns in Base model
        columns = list(
            filter(lambda col: col.name not in base_model_exclude_columns, model.columns))
        base_model_excluded_columns = list(
            filter(lambda col: col.name in base_model_exclude_columns, model.columns))

        model_columns = [(col.name, col.type.python_type) for col in columns]
        full_model_columns = [(col.name, col.type.python_type)
                              for col in base_model_excluded_columns]

        # create annotations
        excluded_annotations = {}
        for column in base_model_excluded_columns:
            excluded_annotations[column.name] = column.type.python_type

        model_annotations = {}
        for column in columns:
            model_annotations[column.name] = column.type.python_type

        # create pydantic Base model
        cls_name = "".join([ n.title() for n in name.split('_')])
        pydantic_model = {"name":str(cls_name)}
        cls_name = f"{cls_name}{base_postfix}"
        
        bases = (BaseModel,)
        base_model = type(cls_name, bases, {})
        for key, val in dict(model_columns).items():
            setattr(base_model, key, None)
        # apply annotations
        setattr(base_model, "__annotations__", model_annotations)
        pydantic_model["base"] = base_model

        # create pydantic Create model
        cls_name = "".join([ n.title() for n in name.split('_')])
        cls_name = f"{cls_name}{create_postfix}"
        bases = (base_model,)
        create_model = type(cls_name, bases, {})
        pydantic_model["create"] = create_model

        # create pydantic full model
        cls_name = "".join([ n.title() for n in name.split('_')])
        cls_name = f"{cls_name}{full_postfix}"
        bases = (base_model,)
        inner_cls = type(
            'Config',
            (),
            {}
        )
        setattr(inner_cls, 'orm_mode', True)
        full_model = type(cls_name, bases, {})
        for key, val in dict(full_model_columns).items():
            setattr(full_model, key, None)
        setattr(full_model, "__annotations__", excluded_annotations)
        setattr(full_model, inner_cls.__name__, inner_cls)
        pydantic_model["full"] = full_model
        pydantic_model["db_class"] = model
        pydantic_models.append(pydantic_model)

    return pydantic_models