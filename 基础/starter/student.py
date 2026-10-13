"""Evidence-grounded message construction for the basic task."""
import re


def _terms(text):
    return re.findall(r"[A-Za-z0-9]+|[\u4e00-\u9fff]", text.lower())


def prepare_messages(question, passages):
    """Build a constrained request using only the supplied question and passages."""
    evidence = "\n\n".join(
        f"[{passage['id']}] source={passage['source']}\n{passage['text']}"
        for passage in passages
    )
    system = (
        "You answer document verification questions using only the evidence supplied by the user. "
        "Do not use outside knowledge. If the evidence is insufficient or conflicting, say so briefly. "
        "Return valid JSON only with exactly these fields: "
        '{"answer":"short answer or evidence insufficient","citations":["passage-id"]}. '
        "Citations must be IDs of passages that directly support the answer."
    )
    user = f"Question:\n{question}\n\nEvidence:\n{evidence}"
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]

def improve(question, passages):
    """Rank supplied evidence by lexical overlap without changing its contents."""
    terms = set(_terms(question))
    indexed = list(enumerate(passages))
    indexed.sort(key=lambda item: (-len(terms.intersection(set(_terms(item[1]['text'])))), item[0]))
    return [passage for _, passage in indexed]
