from blacksheep import Application, post,  FromForm, FromFiles, get
from optimizer import Portfolio
from models import OptimizeParams

app = Application()

@post("/optimize-portfolio")
async def optimize_portafolio(files: FromFiles, params: FromForm[OptimizeParams]):

    file = files.value
    data = file[0].data

    nivel_riesgo = params.value.risk_level
    peso_max     = params.value.max_weight

    portfolio = Portfolio(data)
    optimize = portfolio.optimize(nivel_riesgo, peso_max)
    return  optimize


@get("/")
async def index():
    return "Hello, World!"
