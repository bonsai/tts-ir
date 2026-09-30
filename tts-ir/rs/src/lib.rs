use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "op")]
pub enum Op {
    #[serde(rename = "say")]
    Say { text: String },
    #[serde(rename = "pause")]
    Pause { ms: u64 },
    #[serde(rename = "speaker")]
    Speaker { speaker: String },
    #[serde(rename = "style")]
    Style { style: String },
}

pub fn validate(op: &Op) -> Result<(), String> {
    match op {
        Op::Say { text } => {
            if text.trim().is_empty() { return Err("say.text must be non-empty".into()); }
            if text.contains('<') || text.contains('>') || text.contains('[') || text.contains(']') {
                return Err("say.text contains markup".into());
            }
        }
        Op::Pause { .. } | Op::Speaker { .. } | Op::Style { .. } => {}
    }
    Ok(())
}

pub fn parse_jsonl(input: &str) -> Result<Vec<Op>, String> {
    input.lines().filter(|l| !l.trim().is_empty()).enumerate().map(|(i, l)| {
        let op = serde_json::from_str::<Op>(l).map_err(|e| format!("line {}: {}", i + 1, e))?;
        validate(&op)?;
        Ok(op)
    }).collect()
}
