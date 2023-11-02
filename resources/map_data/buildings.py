import pytmx

class VegetablesMarket:
    def __init__(self, group):
        self.tmx_data = pytmx.util_pygame.load_pygame(
            "util/Portfolio Game Map.tmx")

    def get_tile_image(self):
        market_layer = self.tmx_data.get_layer_by_name("VEGETABLES MARKET FOREGROUND")

        return market_layer
