from sanic import json, Request
from pydantic import ValidationError

from app.forecast import forecast_blueprint
from app.forecast.models import (PredictionInputModel, PredictionErrorResponseModel, PredictionResponseModel,
                                 CumulativePredictionResponseModel)
from app.utils.constans import SYMBOL_NAME_MAPPING, NAME_SYMBOL_MAPPING
from app.utils.errors import extract_message_from_error


@forecast_blueprint.get('/predictions')
async def predictions_view(request: Request):
    try:
        input_model = PredictionInputModel(**request.args)
    except ValidationError as error:
        response_model = PredictionErrorResponseModel(endpoint=request.url,
                                                      message=extract_message_from_error(error),
                                                      status_code=400)
        return json(response_model.dict(), status=response_model.status_code)

    if input_model.symbol == 'ALL':
        predictions = [PredictionResponseModel(name=SYMBOL_NAME_MAPPING[key],
                                               symbol=key,
                                               prediction=request.app.ctx.forecast_dictionary[key].to_dict()
                                               ) for key in request.app.ctx.forecast_dictionary.keys()]

        response_model = CumulativePredictionResponseModel(predictions=predictions)
        return json(response_model.dict())

    prediction = request.app.ctx.forecast_dictionary[input_model.symbol]
    response_model = PredictionResponseModel(name=SYMBOL_NAME_MAPPING[input_model.symbol],
                                             symbol=input_model.symbol,
                                             prediction=prediction.to_dict())
    return json(response_model.dict())
