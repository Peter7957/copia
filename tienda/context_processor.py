def total_carrito(request):
    total = 0
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                total += int(value["acumulado"])
    else:
        carrito = request.session.get("carrito")
        if carrito:
            for key, value in carrito.items():
                total += int(value["acumulado"])
    return {"total_carrito": total}