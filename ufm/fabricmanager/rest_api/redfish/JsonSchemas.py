from flask_restful import Resource

from rest_api.redfish import redfish_constants


class JsonSchemas(Resource):

    def get(self):
        resp = {
            "id": "http://redfish.dmtf.org/schemas/v1/redfish-schema.v1_2_0",
            "type": "object",
            "$schema": "http://redfish.dmtf.org/schemas/v1/redfish-schema.v1_2_0",
            "title": "Redfish Schema Extension",
            "description": "The properties defined in this schema shall adhere to the requirements of the Redfish Specification and the semantics of the descriptions in this file.",
            "allOf": [
                {
                    "$ref": "http://json-schema.org/draft-04/schema"
                }
            ],
            "definitions": {
                "readonly": {
                    "type": "boolean",
                    "description": "This property shall designate a property to be readonly when set to true."
                },
                "requiredOnCreate": {
                    "type": "array",
                    "items": {
                        "type": "boolean"
                    },
                    "description": "This property is required to be specified in the body of a POST request to create the resource."
                },
                "longDescription": {
                    "type": "string",
                    "description": "This attribute shall contain normative language relating to the Redfish Specification and documentation."
                },
                "copyright": {
                    "type": "string",
                    "description": "This attribute shall contain the copyright notice for the schema."
                },
                "deprecated": {
                    "type": "string",
                    "description": "The term shall be applied to a property in order to specify that the property is deprecated.  The value of the string should explain the deprecation, including new property or properties to be used. The property can be supported in new and existing implementations, but usage in new implementations is discouraged.  Deprecated properties are likely to be removed in a future major version of the schema."
                },
                "enumDescriptions": {
                    "type": "object",
                    "description": "This attribute shall contain informative language related to the enumeration values of the property."
                },
                "enumLongDescriptions": {
                    "type": "object",
                    "description": "This attribute shall contain normative language relating to the enumeration values of the property."
                },
                "enumDeprecated": {
                    "type": "object",
                    "description": "The term shall be applied to a value in order to specify that the value is deprecated.  The value of the string should explain the deprecation, including new value to be used.  The value can be supported in new and existing implementations, but usage in new implementations is discouraged.  Deprecated values are likely to be removed in a future major version of the schema."
                },
                "units": {
                    "type": "string",
                    "description": "This attribute shall contain the units of measure used by the value of the property."
                }
            },
            "properties": {
                "readonly": {
                    "$ref": "#/definitions/readonly"
                },
                "longDescription": {
                    "$ref": "#/definitions/longDescription"
                },
                "copyright": {
                    "$ref": "#/definitions/copyright"
                },
                "enumDescriptions": {
                    "$ref": "#/definitions/enumDescriptions"
                },
                "enumLongDescriptions": {
                    "$ref": "#/definitions/enumLongDescriptions"
                },
                "units": {
                    "$ref": "#/definitions/units"
                }
            }
        }

        return resp, redfish_constants.SUCCESS
