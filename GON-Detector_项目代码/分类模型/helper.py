import torch
import time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import torch.nn as nn
try:
    from torch.hub import load_state_dict_from_url
except ImportError:
    from torch.utils.model_zoo import load_url as load_state_dict_from_url


def plot_batch(img_batch,classes,labels=None,preds=None,normalize=False,_mean=[0.485,0.456,0.406],_std=[0.229,0.224,0.225]):
    """
        given a batch of image plot the images with corresponding labels
        img_batch -> batch of image tensor
        classes -> array of class names
        labels -> batch of ground truth corresponding to img_batch
        preds -> predicted batch of labels
        normalize -> (boolean) representing normalized img tensor
    """

    ## parameters w.r.t normalization | change w.r.t img
    mean = np.array(_mean)
    std = np.array(_std)
    ## parameters for plot
    n_rows = 2
    n_cols = len(img_batch)/n_rows 

    fig = plt.figure(figsize=(30,5))

    for idx in range(len(img_batch)):
        ax = fig.add_subplot(n_rows,n_cols,idx+1,xticks=[],yticks=[])
        image = img_batch[idx].numpy().transpose(2,1,0)
        if normalize:
            image = std * image + mean
            image = np.clip(image,0,1)
        ax.imshow(image)
        if labels is not None and preds is not None:
            ax.set_title(f"Predicted: {classes[labels[idx].item()]}",
            c=("green" if labels[idx] == preds[idx] else "red"))
        elif labels is not None:
            ax.set_title(f"Class: {classes[labels[idx].item()]}")


def train(model,trainloader,validloader,optimizer,criterion,epochs=50,device="cpu"):
    """
        given a model, device, dataloaders, optimizer, criterion train the model
        for n epochs and return the train and validation losses. 
    """
    last_loss = np.inf
    train_losses,valid_losses = [],[]

    for e in range(epochs):
        start = time.time()
        train_loss = 0.0
        valid_loss = 0.0
        ## training phase
        model.train()
        for features,labels in trainloader:
            optimizer.zero_grad()
            features,labels = features.to(device),labels.to(device)
            logps = model(features)
            loss = criterion(logps,labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        train_losses.append(train_loss/len(trainloader))

        ## validation phase
        model.eval()
        for features,labels in validloader:
            features,labels = features.to(device),labels.to(device)
            logps = model(features)
            loss = criterion(logps,labels)
            valid_loss += loss.item()
        valid_losses.append(valid_loss/len(validloader))
        
        print(f"epoch: {e+1}/{epochs} trainloss: {train_loss/len(trainloader):.5f} validloss: {valid_loss/len(validloader):.5f} time: {time.time() - start:.3f} sec")

      ## saving model parameters
        if(valid_loss < last_loss):
            print(f"Loss decresed: {last_loss/len(validloader):.5f} -> {valid_loss/len(validloader):.5f}")
            # torch.save(model.state_dict(),"model_weights.pth")
            last_loss = valid_loss
    return (train_losses,valid_losses)




def test(model,testloader,optimizer,criterion,device="cpu"):
    """
        helper function to test the accuracy of trained model
    """
    test_loss = 0.0
    accuracy = 0.0
    model.eval()
    with torch.no_grad():
        for features,labels in testloader:
            features,labels = features.to(device),labels.to(device)
            logps = model(features)
            loss = criterion(logps,labels)
            ps = torch.exp(logps)
            top_p,top_class = ps.topk(1,dim=1)
            equals = top_class == labels.view(*top_class.shape)
            accuracy += torch.mean(equals.type(torch.FloatTensor)).item()
            test_loss += loss.item()

    print(f"testloss: {test_loss/len(testloader):.6f} accuracy: {accuracy/len(testloader):.3f}")


def predict(img,classes,labels,model,device="cpu"):
    """
        function to predict label of input image
    """
    model.eval()
    img = img.to(device)
    output = model(img)
    _,preds = torch.max(output,dim=1)  # value, indices
    img = img.to("cpu")
    plot_batch(img,classes,labels,preds,normalize=True)

def predict_image(image_path,model,transform,device,classes):
    model.eval()
    img = Image.open(image_path)
    plt.imshow(img)
    img_tensor = transform(img)
    # print(img_tensor.shape)
    img_tensor = torch.stack([img_tensor])
    # print(img_tensor.shape)
    img_tensor = img_tensor.to(device)

    output = model(img_tensor)

    _,preds = torch.max(output,dim=1)
    # t = torch.softmax(output,dim=1)
    # print(t[0])
    print('prob:{}%'.format(torch.max(torch.softmax(output,dim=1)).item()*100))

    plt.title(classes[preds.item()])
    plt.show()
