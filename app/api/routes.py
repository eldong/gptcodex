from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.conversion import convert_usd, get_supported_currencies

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _base_context(request: Request) -> dict:
    return {
        "request": request,
        "currencies": get_supported_currencies(),
    }


@router.get("/", response_class=HTMLResponse)
async def get_form(request: Request) -> HTMLResponse:
    context = {
        **_base_context(request),
        "result": None,
        "amount": "",
        "selected_currency": "EUR",
        "error": None,
    }
    return templates.TemplateResponse("index.html", context)


@router.post("/convert", response_class=HTMLResponse)
async def post_convert(
    request: Request,
    amount: str = Form(...),
    currency: str = Form(...),
) -> HTMLResponse:
    context = {
        **_base_context(request),
        "amount": amount,
        "selected_currency": currency,
    }
    try:
        converted = convert_usd(amount, currency)
    except ValueError as exc:
        context.update({"result": None, "error": str(exc)})
    else:
        context.update({"result": f"{converted}", "error": None})
    return templates.TemplateResponse("index.html", context)
