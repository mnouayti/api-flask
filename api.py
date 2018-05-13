# -*- coding: utf-8 -*-

# *****************************************************************************
# IMPORTS
# *****************************************************************************

from datetime import datetime
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from marshmallow import Schema, fields
import hashlib
from flask_cors import CORS

# *****************************************************************************
# MODELS
# *****************************************************************************


class Page(object):

    def __init__(self, title, html, url, created_by, **kwargs):
        self.html = html
        self.created_at = datetime.now()
        self.created_by = created_by
        self.id = hashlib.md5(bytes(url, "utf-8")).hexdigest()
        self.title = title
        self.url = url
        

    def __repr__(self):
        return '<Page(title={self.title!r})>'.format(self=self)


# *****************************************************************************
# SHEMAS
# *****************************************************************************


class PageSchema(Schema):

    html = fields.Str(required=True)
    created_at = fields.DateTime()
    created_by = fields.Str(required=True)
    id = fields.Str()
    title = fields.Str(required=True)
    url = fields.Url(required=True)


# *****************************************************************************
# RESOURCES
# *****************************************************************************


class Pages(Resource):

    def get(self, id=None):
        data = []
        if id:
            page = mongo.db.pages.find_one({"id": id}, {"_id": 0})
            if page:
                return jsonify({"message": "ok", "data": page})
            else:
                return {"message": "no page found for {}".format(id)}, 404
        else:
            pages = mongo.db.pages.find({}, {"_id": 0})
            if pages:
                for page in pages:
                    data.append(page)
                return jsonify({"message": "ok", "data": data})
            else:
                return {"message": "The database is empty"}, 404

    def post(self):
        data = request.get_json()
        result = PageSchema().load(data)
        if result.errors:
            return result.errors, 400
        else:
            page = Page(**result.data)
            if mongo.db.pages.find_one({"id": page.id}):
                return {"message": "Page already exists."}, 400
            else:
                mongo.db.pages.insert(PageSchema().dump(page).data)
                return {"message": "ok", "id": page.id}, 201


# *****************************************************************************
# API INITIALIZATION
# *****************************************************************************


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config["MONGO_DBNAME"] = "pages_db"
app.config["MONGO_HOST"] = "mongo"
mongo = PyMongo(app, config_prefix='MONGO')
api = Api(app)
api.add_resource(Pages, "/api/pages", endpoint="pages")
api.add_resource(Pages, "/api/pages/<string:id>", endpoint="id")


# *****************************************************************************
# MAIN
# *****************************************************************************


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
