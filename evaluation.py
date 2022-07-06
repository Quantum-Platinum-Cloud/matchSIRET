from typing import List
from api_calls import annuaire_entreprise, social_gouv

def score_companies(algorithm: str, sirens: List[str], names: List[str], zipcodes: List[str]):
    algorithm = algorithm.lower()
    known_services = ["annuaire-entreprises", "social-gouv"]
    assert algorithm in known_services, f"The service {algorithm} is unknown. Please choose one of these: {known_services}"
    assert len(sirens) == len(names) and len(names) == len(zipcodes), "Error in input data: sirens, names and zipcodes must have same lengths."
    score = 0
    for k, name in enumerate(names):
        zipcode = str(zipcodes[k])
        if algorithm == "annuaire-entreprises":
            found_sirens, found_names, found_usual_names = annuaire_entreprise(name=name,zipcode=zipcode)
        elif algorithm == "social-gouv":
            found_sirens, found_names, found_usual_names = social_gouv(name=name, address=zipcode)
        try:
            most_probable_siren = found_sirens[0]
            score += (most_probable_siren == sirens[k])
        except IndexError:
            continue
    return score / max(len(sirens),1)
    