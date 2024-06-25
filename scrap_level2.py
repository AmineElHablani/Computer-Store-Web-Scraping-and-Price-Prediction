from bs4 import BeautifulSoup, NavigableString, Tag
import re 
import requests
import csv


#Mytek 
site="https://www.mytek.tn/informatique/ordinateurs-portables/pc-portable.html?"

#Columns
csv_columns=['name','price','image','description','DISPONIBILITÉ','gtin','Marque','Gamme PC','Gamer',"Système d'exploitation","Taille de l'écran","Ecran","Ecran Tactile","Résolution Ecran","Processeur","Type Processeur","Référence Processeur","Fréquence Processeur","Mémoire Cache","Mémoire","Disque Dur","Type Disque Dur","Carte Graphique","Chipset Graphique","Clavier","Connecteurs","Destockage","Couleur","Garantie"]
features_columns=['DISPONIBILITÉ','gtin','Marque','Gamme PC','Gamer',"Système d'exploitation","Taille de l'écran","Ecran","Ecran Tactile","Résolution Ecran","Processeur","Type Processeur","Référence Processeur","Fréquence Processeur","Mémoire Cache","Mémoire","Disque Dur","Type Disque Dur","Carte Graphique","Chipset Graphique","Clavier","Connecteurs","Destockage","Couleur","Garantie"]
filecsv=open("mytek_laptop_full_features.csv","w",encoding='utf-8')
writer=csv.DictWriter(filecsv,fieldnames=csv_columns)
writer.writeheader()

for page in range(1,33):
    allsite=[]
    print('-- page:',page,'--')
    if page==1:
        page=''
    else:
        page='p='+str(page)
    
    r=requests.get(site+page)
    print(site+page)
    
    
    soup=BeautifulSoup(r.content,'html.parser')
    #get only product elements
    #for body_child in soup.body.children:
    #try:
    product_elements =soup.find('ol',{'products list items product-items'})
    #get all the links
    #if product_elements:
    anchor=product_elements.findAll('a',attrs={'href':re.compile("^https:")})

    for link in anchor:
        if len(link.get('href')) <= 30:
            pass 
        else:
            allsite.append(link.get('href'))

    #print('taille:',len(allsite),':',allsite)
    #print([len(i) for i in allsite])
    unique_site=[]
    for element in allsite:
        if element not in unique_site:
            unique_site.append(element)
    
    #print('unique list:',len(unique_site))
    #print(unique_site)



    #get inside each list
    for idx,l in enumerate(unique_site):
        print('--element:',idx+1,'--')

        r = requests.get(l)
        soup=BeautifulSoup(r.content,"html.parser")
        #anchor=soup.find('div',{'column main'})

        name= soup.find('h1',{'page-title'})
        
        price_div=soup.find('div',{'product-info-price'})
        price=price_div.find('span','price')
        
        img_div=soup.find('div',attrs={'class':'carousel-item active'})
        image = img_div.find('img', attrs={'id': 'productimg'})
        
        description_div=soup.find('div',{'product attribute overview'})
        description=description_div.find('div',{'value'})
        #print(name.text)
        #price=anchor.find('div',{'price-box price-final_price'})
        #print('#####')
        #print(image)

        features=[]
        features_label=[]
        anchor_table=soup.find('table',{'data table additional-attributes'})
        #if anchor_table:
        anchor_features=anchor_table.find_all('tr',attrs={})
        for f in anchor_features:
            features.append(f.find('td',{'col data'}).text )
            features_label.append(f.find('th',{'col label'}).text )
        #print(features)
        if  features_label[-5]!="Clavier":
            features_label.insert(-5,'Clavier')
            features.insert(-5,None)
        
        if features_label[1]!='gtin':
            features_label.insert(1,'gtin')
            features.insert(1,None)
        
        #Add null values for non-existing features
        for idx,e in enumerate(features_columns):
            if e not in features_label:
                features_label.insert(idx,e)
                features.insert(idx,None)
                
        #Delete the unnecessary features
        for idx,e in enumerate(features_label):
            if e not in csv_columns:
                features_label.pop(idx)
                features.pop(idx)
            
 
        if image:
            writer.writerow({
                'name':name.text,
                'price':price.text,
                'image':image.get('src'),
                'description':description.text,
                features_label[0]:features[0],
                features_label[1]:features[1],
                features_label[2]:features[2],
                features_label[3]:features[3],
                features_label[4]:features[4],
                features_label[5]:features[5],
                features_label[6]:features[6],
                features_label[7]:features[7],
                features_label[8]:features[8],
                features_label[9]:features[9],
                features_label[10]:features[10],
                features_label[11]:features[11],
                features_label[12]:features[12],
                features_label[13]:features[13],
                features_label[14]:features[14],
                features_label[15]:features[15],
                features_label[16]:features[16],
                features_label[17]:features[17],
                features_label[18]:features[18],
                features_label[19]:features[19],
                features_label[20]:features[20],
                features_label[21]:features[21],
                features_label[22]:features[22],
                features_label[23]:features[23],
                features_label[24]:features[24],

            })

   # except : 
   #     pass        


filecsv.close()
        

        
        

        