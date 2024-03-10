from flask import Blueprint, render_template, redirect, url_for, current_app, request, session

from src.utils.login_required import login_required
from src.app.price_predictions.models.prediction import Prediction
from src.utils.dataset_feature_names import DatasetFeatureNames


car_price_blue_print = Blueprint(
    name="price_predictions",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/price-predictions"
)


@car_price_blue_print.route("car-price-form", methods=["GET"])
@login_required
def get_price_form():
    import pandas as pd
    df = pd.read_csv("data/dataset_raw/train.csv")

    price_params = {}
    for column in DatasetFeatureNames.get_ids():
        df[column] = df.pop(column.replace("_", ""))

        if df[column].dtype == 'object' or column == 'symboling':
            price_params[column+"s"] = df[column].unique().tolist()

    price = request.args.get("price")
    if price is not None:
        price_params['price'] = price

    return render_template("form_base.html", **price_params)


@car_price_blue_print.route("get-car-price", methods=["POST"])
@login_required
def get_price():
    price = 0
    price_params = {}

    price_params.update(request.form)
    price_params['price'] = price
    if session.get("user_id") is not None:
        price_params["user_id"] = session.get("user_id")

    new_prediction = Prediction(**price_params)
    current_app.logger.info(f"Was completed prediction: {new_prediction}")
    new_prediction.save()

    return redirect(url_for("price_predictions.get_price_form", price=price))
