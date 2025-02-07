from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer

# Load Dataset
dataset = load_dataset("ag_news")
train_data = dataset["train"].shuffle(seed=42).select(range(10000))

# Load Pretrained Model
model_name = "facebook/opt-1.3b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Training Arguments
training_args = TrainingArguments(
    output_dir="D:\Geo LLM\src/output",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    num_train_epochs=3,
    logging_dir="D:\Geo LLM\src/logs",
    save_strategy="epoch",
)

# Train Model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,

    tokenizer=tokenizer,
)
trainer.train()

# Save Model
model.save_pretrained("D:\Geo LLM\src/fine_tuned_model")
tokenizer.save_pretrained("D:\Geo LLM\src/fine_tuned_model")
