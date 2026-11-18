
from flask import Flask, request, jsonify
from zeep import Client
from zeep.exceptions import Fault, TransportError
from zeep.transports import Transport
from requests import Session

app = Flask(__name__)

WSDL_URL = (
    "https://www.dataaccess.com/webservicesserver/"
    "NumberConversion.wso?WSDL"
)


def validate_number(value):
    """Validate the input before calling the SOAP service."""
    if isinstance(value, bool):
        raise ValueError("Number must be a whole number, not a boolean.")

    if isinstance(value, int):
        number = value
    elif isinstance(value, str) and value.isascii() and value.isdecimal():
        number = int(value)
    else:
        raise ValueError("Number must contain whole-number digits only.")

    if not 1 <= number <= 1000000:
        raise ValueError("Number must be between 1 and 1,000,000.")

    return number


def convert_number(value):
    """Call the public SOAP service and return a Python dictionary."""
    number = validate_number(value)

    session = Session()
    session.verify = True

    transport = Transport(session=session, timeout=10)

    client = Client(wsdl=WSDL_URL, transport=transport)

    result = client.service.NumberToWords(ubiNum=number)

    if not isinstance(result, str) or not result.strip():
        raise ValueError("SOAP service returned an invalid response.")

    return {
        "number": number,
        "words": result.strip()
    }


def handle_conversion(value):
    try:
        result = convert_number(value)
        return jsonify(result), 200

    except ValueError as exc:
        return jsonify({
            "error": f"Custom validation error: {exc}"
        }), 400

    except Fault as exc:
        return jsonify({
            "error": f"Custom SOAP service fault: {exc}"
        }), 502

    except (TransportError, OSError) as exc:
        return jsonify({
            "error": f"Custom SOAP connection error: {exc}"
        }), 502

    except Exception as exc:
        app.logger.exception("Unexpected SOAP client error")
        return jsonify({
            "error": f"Custom application error: {exc}"
        }), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "SOAP Number Conversion API",
        "get_example": "/convert?number=123",
        "post_endpoint": "/convert",
        "post_example": {"number": 123}
    })


@app.route("/convert", methods=["GET"])
def convert_get():
    number = request.args.get("number")
    return handle_conversion(number)


@app.route("/convert", methods=["POST"])
def convert_post():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Custom validation error: Send a JSON object."
        }), 400

    return handle_conversion(data.get("number"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
