from decimal import Decimal


def observation_meets_spec(observation: str, format: str, specification: str) -> bool:
    if format.startswith("decimal"):
        obs_val = Decimal(observation)

        if len(tokens := format.split(":")) > 1:
            places = int(tokens[1])
            obs_val.quantize(Decimal(f"0.{'0' * places}"))

        print(obs_val)

    if specification.startswith("[") and specification.endswith("]"):
        tokens = [token.strip() for token in specification[1:-1].split(",")]
        spec_min = Decimal(tokens[0])
        spec_max = Decimal(tokens[1])

        return obs_val >= spec_min and obs_val <= spec_max

    return False
