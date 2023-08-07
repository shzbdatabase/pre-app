from pydantic import BaseModel


class TradeResample(BaseModel):
    # trade id
    I_min: int
    I_max: int

    # price
    p_first: float
    p_last: float
    p_min: float
    p_max: float
    p_sum: float
    p_avg: float
    # amount
    a_first: float
    a_last: float
    a_min: float
    a_max: float
    a_sum: float
    a_avg: float
    # cost
    q_first: float
    q_last: float
    q_min: float
    q_max: float
    q_sum: float
    q_avg: float
    # side
    m_sum: int

    # resample count
    cnt: int
    # timestamp
    t: int
    t_min: int
    t_max: int
    # insert timestamp
    i: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "t": 1691050602000,
                "I_min": "278209881",
                "I_max": "278209882",
                "t_min": 1691050602167,
                "t_max": 1691050602304,
                "p_first": 227.63,
                "p_last": 227.63,
                "p_min": 227.63,
                "p_max": 227.63,
                "p_sum": 455.26,
                "p_avg": 227.63,
                "a_first": 16.339,
                "a_last": 0.057,
                "a_min": 0.057,
                "a_max": 16.339,
                "a_sum": 16.395999999999997,
                "a_avg": 8.197999999999999,
                "q_first": 3719.24657,
                "q_last": 12.97491,
                "q_min": 12.97491,
                "q_max": 3719.24657,
                "q_sum": 3732.2214799999997,
                "q_avg": 1866.1107399999999,
                "m_sum": 0,
                "cnt": 2,
            }
        }
    }
