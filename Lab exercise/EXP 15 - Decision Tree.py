
# Decision Tree Implementation

# Dataset: [Outlook, Wind]
# Outlook: 0 = Sunny, 1 = Rainy
# Wind: 0 = Weak, 1 = Strong
# Play: 1 = Yes, 0 = No

data = [
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 1],
    [1, 1, 0]
]

def predict(outlook, wind):
    if outlook == 0:
        if wind == 0:
            return "Yes"
        else:
            return "No"
    else:
        if wind == 0:
            return "Yes"
        else:
            return "No"

print("Decision Tree Prediction")
print("------------------------")

outlook = int(input("Enter Outlook (0=Sunny, 1=Rainy): "))
wind = int(input("Enter Wind (0=Weak, 1=Strong): "))

if outlook not in (0, 1) or wind not in (0, 1):
    print("Invalid input!")
else:
    result = predict(outlook, wind)
    print("Play Cricket:", result)
