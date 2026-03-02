import pandas as pd 
import streamlit   as st
import pickle as pkl

def classifier(x):
    if x >= 12:
        return ">= 12"
    elif x >= 8 :
        return "[8-12["
    elif x >= 4 :
        return "[4-8["
    else:
        return "< 4"


rgs = pkl.load(open("regression_model.pkl","rb"))
model = rgs["model"]
scaler = rgs["scaler"]
ordinal_encoder = rgs["ordinal_encoder"]
label_encoder = rgs["label_encoder"]

def regression_pedict(f:dict):
    classified = []
    for x in ['BedroomAbvGr', 'TotRmsAbvGrd', 'OverallQual', 'OverallCond']:
        f[x] = classifier(f[x])
        classified.append(f[x])
    encoded = ordinal_encoder.transform([classified])
    for x in ['BedroomAbvGr', 'TotRmsAbvGrd', 'OverallQual', 'OverallCond']:
        f[x] = encoded[x][0]
    f["Neighborhood"] = label_encoder.transform([f["Neighborhood"]])[0]
    d = pd.DataFrame([f])
    d["SalePrice"] = 0 #juste pour pouvoir scale
    d = scaler.transform(d)
    d.drop(["SalePrice"],axis=1,inplace=True)
    y_pred = model.predict(d)
    d["SalePrice"] = y_pred[0]
    res = scaler.inverse_transform(d)
    prix = res[0][-1]
    return prix


cls =  pkl.load(open("classification_model.pkl","rb"))
model2 = cls["model"]
scaler2 = cls['scaler']
Neighborhood_label_encoder = cls['Neighborhood_label_encoder']
BldgType_label_encoder = cls["BldgType_label_encoder"]
HouseStyle_one_hot_encoder  = cls["HouseStyle_one_hot_encoder"]


def class_predict(f2):
    f2["Neighborhood"] = Neighborhood_label_encoder.transform([f2["Neighborhood"]])[0]
    encoded = HouseStyle_one_hot_encoder.transform([[f2["HouseStyle"]]])
    f2["BldgType"] = 0
    d2 = pd.DataFrame([f2])
    d2 = pd.concat([d2,encoded],axis=1).drop(["HouseStyle"], axis=1)
    d2 = scaler2.transform(d2)
    d2.drop(["BldgType"],axis=1,inplace=True)
    y_pred2 = int(model2.predict(d2)[0])
    tp = BldgType_label_encoder.inverse_transform([y_pred2])[0]
    return tp


quartier = ['CollgCr', 'Veenker', 'Crawfor', 'NoRidge', 'Mitchel', 'Somerst',
       'NWAmes', 'OldTown', 'BrkSide', 'Sawyer', 'NridgHt', 'NAmes',
       'SawyerW', 'IDOTRR', 'MeadowV', 'Edwards', 'Timber', 'Gilbert',
       'StoneBr', 'ClearCr', 'NPkVill', 'Blmngtn', 'BrDale', 'SWISU',
       'Blueste']
htypes = ['2Story', '1Story', '1.5Fin', '1.5Unf', 'SFoyer', 'SLvl', '2.5Unf',
       '2.5Fin']
btypes = ['1Fam', '2fmCon', 'Duplex', 'TwnhsE', 'Twnhs']
with st.sidebar:
    op = ["Prédiction du prix de la maison","Prédiction du type de bâtiment"]
    choix = st.selectbox("Menu",[0,1],format_func=lambda x: op[x])
st.markdown("<h1>Dream House</h1>", unsafe_allow_html=True)

if choix == 0:
    st.write("Entrez les informations pour prédire le prix d'une maison.")
    form = st.form("regressor")
    with form:
        GrLivArea = st.number_input("GrLivArea")
        TotalBsmtSF = st.number_input("TotalBsmtSF")
        LotArea = st.number_input("LotArea")
        BedroomAbvGr = int(st.number_input("BedroomAbvGr", step=1))
        FullBath = int(st.number_input("FullBath", step=1))
        TotRmsAbvGrd = int(st.number_input("TotRmsAbvGrd", step=1))
        OverallQual = int(st.number_input("OverallQual", step=1))
        OverallCond = int(st.number_input("OverallCond", step=1))
        YearBuilt = int(st.number_input("YearBuilt", 1700, 2026))
        YearRemodAdd = int(st.number_input("YearRemodAdd", 1700, 2026))
        Neighborhood = st.selectbox("Quartier", quartier)
        GarageCars = int(st.number_input("GarageCars", step=1))
        GarageArea = st.number_input("GarageArea")
        PoolArea = st.number_input("PoolArea")
        Fireplaces = int(st.number_input("Fireplaces", step=1))

        regressor_submited = st.form_submit_button("Prédire")

    if regressor_submited:
        f = {
            "GrLivArea": GrLivArea,
            "TotalBsmtSF": TotalBsmtSF,
            "LotArea": LotArea,
            "BedroomAbvGr": BedroomAbvGr,
            "FullBath": FullBath,
            "TotRmsAbvGrd": TotRmsAbvGrd,
            "OverallQual": OverallQual,
            "OverallCond": OverallCond,
            "YearBuilt": YearBuilt,
            "YearRemodAdd": YearRemodAdd,
            "Neighborhood": Neighborhood,
            "GarageCars": GarageCars,
            "GarageArea": GarageArea,
            "PoolArea": PoolArea,
            "Fireplaces": Fireplaces
        }

        
        pred = regression_pedict(f)
        st.success(f"Prix prédit : {pred}")
elif choix == 1:
    st.write("Entrez les informations pour prédire le type de bâtiment.")
    form = st.form("classifier_form")
    with form:
        GrLivArea = st.number_input("GrLivArea") ###
        TotRmsAbvGrd = int(st.number_input("TotRmsAbvGrd", step=1))
        OverallQual = int(st.number_input("OverallQual", step=1))
        YearBuilt = int(st.number_input("YearBuilt", 1700, 2026))
        GarageCars = int(st.number_input("GarageCars", step=1))
        Neighborhood = st.selectbox("Quartier", quartier)
        HouseStyle = st.selectbox("House Type", htypes)
        

        classifier_submited = st.form_submit_button("Prédire")
    if classifier_submited:

        f2 = {
        'GrLivArea': GrLivArea, ###
        'TotRmsAbvGrd':TotRmsAbvGrd, ###
        'OverallQual':OverallQual, ###
        'YearBuilt':YearBuilt, ###
        'GarageCars':GarageCars,###
        'Neighborhood':Neighborhood, ###
        'HouseStyle':HouseStyle
        
        }
        pred = class_predict(f2)
        st.success(f"Le type de bâtiment est {pred}")