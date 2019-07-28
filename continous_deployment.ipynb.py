#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pwd')


# In[2]:


cd /Users/wanzin/downloads/dl_medical_image


# In[3]:


get_ipython().system('pwd')


# In[4]:


get_ipython().system('tar -zcvf train_model.tgz train_model.h5')


# In[5]:


get_ipython().system('ls -l')


# In[6]:


# Create a Watson Machine Learning client instance
from watson_machine_learning_client import WatsonMachineLearningAPIClient
wml_credentials = {
    "apikey"    : "i2xzr3QtHkfny2iekPlN5T0-qONn4qkHYSUaUPU0tG0F",
    "instance_id" : "455fe1c1-4c6d-4ead-aa98-fee55eb73129",
    "url"    : "https://us-south.ml.cloud.ibm.com"
}
client = WatsonMachineLearningAPIClient( wml_credentials )


# In[9]:


metadata = {
    client.repository.ModelMetaNames.NAME: "keras model",
    client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
    client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.5",
    client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES: [{'name':'keras', 'version': '2.2.4'}]}
model_details = client.repository.store_model( model="train_model.tgz", meta_props=metadata )


# In[10]:


model_id = model_details["metadata"]["guid"]
deployment_details = client.deployments.create( artifact_uid=model_id, name="Keras deployment" )


# In[13]:


from watson_machine_learning_client import WatsonMachineLearningAPIClient
creds = {
}
client = WatsonMachineLearningAPIClient(creds)
metadata = {
    client.repository.ModelMetaNames.NAME: "keras model",
    client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
    client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.5",
    client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES: [
        {'name': 'keras', 'version': '2.2.4'}]
}

model_details = client.repository.store_model(
    model="train_model.tgz", meta_props=metadata)

model_id = model_details["metadata"]["guid"]
print(model_id)
model_deployment_details = client.deployments.create( artifact_uid=model_id, name="ucb_malaria_model" )

print(model_details)
print(model_deployment_details)


# In[17]:


print(model_details)


# In[18]:


model_deployment_details = client.deployments.create( artifact_uid=model_id, name="ucb_malaria_model" )


# In[16]:


print(model_id)


# In[ ]:





# In[19]:


print(model_deployment_details)


# In[14]:


client.deployments.list(
)


# In[15]:


model_endpoint_url = client.deployments.get_scoring_url( deployment_details )
payload = { "values" : image.tolist() }
client.deployments.score( model_endpoint_url, payload )


# In[ ]:




