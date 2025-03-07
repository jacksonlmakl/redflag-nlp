from .agent import agentic_analysis
from .fraud import fraud_analysis
from .context import calculate_context_multiplier
import json

class RedFlag:
    def __init__(self, text_body):
        self.text_body = text_body
        # print(text_body)
        agentic=agentic_analysis(text_body)
        self.agentic_analysis = agentic
        self.fraud_analysis = fraud_analysis(text_body)
        self.context_multiplier = calculate_context_multiplier(text_body)
        self.summary = agentic
        self.summary['_temp']='1'
        self.summary=self.summary.groupby("_temp", as_index=False).max()
        self.summary
        del self.summary['_temp']
        del self.agentic_analysis['_temp']
        # del self.summary['evidence']
        if len(self.fraud_analysis)>0:
            self.summary['contains_external_links']=True
        else:
            self.summary['contains_external_links']=False
        self.summary['text_body']=text_body
        self.base_score=self.compute_bias_fallacy_score()
        self.score=self.base_score*self.context_multiplier
        self.summary['score'] = self.score*100 if self.score*100 <=100 else 100
        
        self.summary=self.summary[['text_body', 'score', 'affirming_the_consequent',	'confirmation_bias',	'optimism_bias',	'availability_bias',	'anchoring_bias',	'framing_bias',	'denying_the_antecedent',	'appeals_to_emotion',	'red_hering',	'straw_man','appealing_to_authority',"obfuscation","dysphemism","euphemism","cherry_picking",'appealing_to_pity',
'virtue_signaling',	'contains_external_links']]
        

    def compute_bias_fallacy_score(self):
        """
        Converts a raw bias/fallacy score into a normalized 0-1 range.
        Ensures severe bias-heavy texts receive appropriately high scores.
        """
        with open("agent_config.json") as f:
            agent_config = json.load(f)
    
        bias_config = agent_config.get("biases", [])
        logic_config = agent_config.get("logic", [])
        config = bias_config + logic_config
    
        col_names = list(self.summary.columns)
        for col in col_names:
            if col not in ("text_body", "evidence"):
                if col != "contains_external_links":
                    weight = next((i["weight"] for i in config if i["column_name"] == col), 5)
                else:
                    weight = 5
                self.summary[col] = self.summary[col].astype(int) * weight
    
        # Sum of all weighted bias/fallacy occurrences
        raw_score = int(
            self.summary[
                [
                    "affirming_the_consequent",
                    "confirmation_bias",
                    "optimism_bias",
                    "availability_bias",
                    "anchoring_bias",
                    "framing_bias",
                    "denying_the_antecedent",
                    "appeals_to_emotion",
                    "red_hering",
                    "straw_man",
                    "appealing_to_authority",
                    "obfuscation",
                    "dysphemism",
                    "euphemism",
                    "cherry_picking",
                    "appealing_to_pity",
                    "virtue_signaling",
                    "contains_external_links",
                ]
            ].values.sum()
        )
    
        # **NEW**: Dynamically determine a more accurate max score
        max_possible_score = min(150, raw_score * 1.1)  # Allows high scores to stay impactful
    
        # **NEW**: Use a smoother normalization with a direct boost for high scores
        if raw_score == 0:
            return .1
        base_score = raw_score / max_possible_score
    
        # **NEW**: Apply stronger boost for severe misinformation cases
        if raw_score > 80:
            base_score = max(base_score, 0.75)  # Ensure high scores don’t get suppressed
    
        if raw_score > 100:
            base_score = max(base_score, 0.9)  # Extreme cases should be close to 1
    
        return round(min(1, base_score), 4)  # Ensure max is capped at 1
