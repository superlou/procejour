from decimal import Decimal


def observation_meets_spec(observation: str, format: str, specification: str) -> bool:
    obs_val = observation_value(observation, format)

    if specification.startswith("[") and specification.endswith("]"):
        tokens = [token.strip() for token in specification[1:-1].split(",")]
        spec_min = Decimal(tokens[0])
        spec_max = Decimal(tokens[1])

        return obs_val >= spec_min and obs_val <= spec_max

    return False


def observation_value(observation: str, format: str) -> Decimal:
    if format.startswith("decimal"):
        obs_val = Decimal(observation)

        parts = format.split(" ")
        numeric_type, unit = parts if len(parts) == 2 else (parts[0], None)

        if len(tokens := numeric_type.split(":")) > 1:
            places = int(tokens[1])
            obs_val.quantize(Decimal(f"0.{'0' * places}"))

        return obs_val
    else:
        raise TypeError("Observation was not numeric")
