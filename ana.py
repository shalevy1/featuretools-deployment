import featuretools as ft
import pandas as pd
from featuretools.primitives import make_agg_primitive
from featuretools.variable_types import Numeric


def feat(data, index="id", date="DATA", agrupada="Item_Name"):
    es = ft.EntitySet(id="Dados")

    if date is None:
        es = es.entity_from_dataframe(entity_id="entidade", dataframe=data, make_index=True, index=index)
    else:
        es = es.entity_from_dataframe(entity_id="entidade", dataframe=data, make_index=True, index=index, time_index=date)

    if agrupada:
        es.normalize_entity(new_entity_id="normal", base_entity_id="entidade", index=agrupada)

    return data, es


def amplitude(values):
    """Criar primitiva de amplitude"""
    amp = values.max() - values.min()
    return amp


Amplitude = ft.primitives.make_agg_primitive(
    amplitude,
    input_types=[Numeric],
    return_type=Numeric,
    name="amplitude",
    description="Calcula a amplitude geral de cada variável numérica",
    cls_attributes=None,
    uses_calc_time=False,
    commutative=False,
    number_output_features=1
)


def agg_features(es):
    feature_matrix, feature_defs = ft.dfs(
        entityset=es,
        target_entity="entidade",
        agg_primitives=[
            Amplitude,
            "avg_time_between",
            "mean",
            "median",
            "std",
            "sum"
        ],
        verbose=True
    )
    return feature_matrix, feature_defs


def transf_features(es):
    feature_matrix, feature_defs = ft.dfs(
        entityset=es,
        target_entity="entidade",
        trans_primitives=[
            "second",
            "hour",
            "year",
            "time_since_previous",
            "diff",
            "day",
            "month",
            "weekday",
            "minute"
        ],
        verbose=True,
        max_depth=1
    )
    return feature_matrix, feature_defs
