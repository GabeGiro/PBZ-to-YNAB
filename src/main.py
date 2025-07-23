from util import extract_transactions_from_image

df = extract_transactions_from_image("your_image.png")
df.to_csv("transactions.csv", index=False)
print(df)