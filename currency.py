from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from . import libs

bp = Blueprint('currency', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/', methods =('GET', 'POST'))
@login_required
def getCurrency():
    if request.method == 'POST':
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        error = None
        if not startDate or not endDate:
            error = 'Both dates are required'
        if error is not None:
            flash(error)
        else:
            cur = libs.getCurrencyFromBankApi(startDate=startDate,
                                           endDate=endDate)
            libs.writeResToGoogleSheet(cur)
            return render_template('success.html')
    return render_template('index.html')