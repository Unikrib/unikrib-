#!/usr/bin/python3

from models.v2.base_model import BaseModel


class House(BaseModel):
    __tablename__ = 'houses'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_params = {"price": "Price", "apartment": "Apartment type",
                            "owner_id": "Owner id",}
        
        for key, val in required_params.items():
            if key not in kwargs:
                raise ValueError(f"{val} parameter is missing")
            
        init_params = {"price": "Price", "agent_fee": "Agent fee",
                      "daily_power": "Daily power", "no_clicks": "Number of clicks",
                      "rooms_available": "Rooms available"}
        for key, val in init_params.items():
            value = getattr(self, key)
            if value is None:
                continue
            if not isinstance(value, int):
                try:
                    if isinstance(value, str):
                        setattr(self, key, int(value))
                    elif isinstance(value, float):
                        pass
                except Exception as e:
                    raise TypeError(f"{val} must be a number")
       
        if kwargs['apartment'] not in ['Single-room', 'Self-contain', 'One-bedroom',
                                       'Two-bedroom', 'Three-bedroom']:
            raise ValueError("Invalid apartment type passed")
        
        if self.running_water in kwargs and self.running_water not in ['yes', 'no']:
            raise ValueError("Running water can only be yes or no")
        if self.waste_disposal in kwargs and self.waste_disposal not in ['yes', 'no']:
            raise ValueError("Waste disposal value can only be yes or no")
        
        default_values = {"newly_built": False, "tiled": False, 'rooms_available': 1,
                          'security_available': False, 'daily_power': 12, 'no_clicks': 0,
                          'image1': 'images/white_image.jpg', 'image2': 'images/white_image.jpg',
                          'image3': 'images/white_image.jpg'}
        for key, val in default_values.items():
            if key not in kwargs or kwargs[key] == "":
                setattr(self, key, val)