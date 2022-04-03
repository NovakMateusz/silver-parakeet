from sanic import json, Request
from pydantic import ValidationError

from app.forecast import forecast_blueprint
from app.forecast.models import (PredictionInputModel, PredictionErrorResponseModel, PredictionResponseModel,
                                 CumulativePredictionResponseModel)
from app.utils.constans import CODE_NAME_MAPPING
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

    if input_model.code == 'ALL':
        predictions = [PredictionResponseModel(name=CODE_NAME_MAPPING[key],
                                               code=key,
                                               prediction=request.app.ctx.forecast_dictionary[key].to_dict()
                                               ) for key in request.app.ctx.forecast_dictionary.keys()]

        response_model = CumulativePredictionResponseModel(predictions=predictions)
        return json(response_model.dict())

    prediction = request.app.ctx.forecast_dictionary[input_model.code]
    response_model = PredictionResponseModel(name=CODE_NAME_MAPPING[input_model.code],
                                             code=input_model.code,
                                             prediction=prediction.to_dict())
    return json(response_model.dict())
