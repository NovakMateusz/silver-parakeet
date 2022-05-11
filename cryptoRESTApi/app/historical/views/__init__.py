from sanic import json, Request
from pydantic import ValidationError

from app.historical import historical_data_blueprint
from app.historical.models import (HistoricalDataInputModel, HistoricalDataErrorResponseModel,
                                   HistoricalDataResponseModel)
from app.utils.errors import extract_message_from_error
from app.utils.constans import CODE_NAME_MAPPING


@historical_data_blueprint.get('/history')
async def historical_data_view(request: Request):
    try:
        input_model = HistoricalDataInputModel(**request.args)
    except ValidationError as error:
        response_model = HistoricalDataErrorResponseModel(endpoint=request.url,
                                                          message=extract_message_from_error(error),
                                                          status_code=400)
        return json(response_model.dict(), status=response_model.status_code)

    historical_data_df = request.app.ctx.historical_data[input_model.code]
    response_model = HistoricalDataResponseModel(name=CODE_NAME_MAPPING[input_model.code],
                                                 code=input_model.code,
                                                 history=historical_data_df.to_dict())
    return json(response_model.dict())
