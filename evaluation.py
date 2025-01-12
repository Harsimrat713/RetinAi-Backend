import torch
from PIL import Image
from glaucoma_model import GlaucomaDiagnoser
import torchvision.transforms as transforms

def extract_green_channel(x):
    return x[1:2, :, :]

def setupModel(model_path, base_model, device):
    # set up the model for evaluation
    model = GlaucomaDiagnoser(base_model=base_model)
    checkpoint = torch.load(model_path, map_location=device, weights_only=False)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    return model

def setup_transforms(image_size):
    # setup transformer for images
    transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Lambda(extract_green_channel), 
        # transforms.Normalize(mean=[0.395, 0.395, 0.395], std=[0.182, 0.182, 0.182]) 
        transforms.Normalize(mean=[0.456], std=[0.224])
    ])
    return transform

def evaluationModel(ImagePath, model, transform):
    image = Image.open(ImagePath).convert("RGB")

    # Convert the image to a PyTorch tensor using transformer
    input_tensor = transform(image)
    input_tensor = input_tensor.unsqueeze(0)
    
    outputs = model(input_tensor)
    _, predicted = torch.max(outputs.data, 1)
    return predicted.item()

def evaluation(imageLocation, sessionInfo):
    # get device info
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # image size
    image_size=224
    # base models
    base_model='tf_mobilenetv3_small_100'
    # base_model='resnet50'
    # location of model weights
    modelPath = 'models/mobilenetv3_94.pth'
    # modelPath = 'models/resnet50_87.pth'
    # setup for model
    transform = setup_transforms(image_size)
    model = setupModel(modelPath, base_model, device)

    for imageInfo in sessionInfo:
        if imageInfo['cropped'] == True:
            prediction = evaluationModel(f'{imageLocation}/cropped_{imageInfo['name']}', model, transform)

            match prediction:
                case 0:
                    imageInfo['prediction'] = 'Normal'
                    # print("Diagnosis: Normal")
                case 1:
                    imageInfo['prediction'] = 'Glaucoma'
                    # print("Diagnosis: Glaucoma")
                case _:
                    imageInfo['prediction'] = 'Unknown'
                    # print("Diagnosis: Unknown")
    return sessionInfo

'''
# for testing
def main():
    sessionInfo = [{'name': 'Corolla GR.jpg', 'cropped': False, 'score': 0, 'selectedForDisp': False}, 
                {'name': '937_left.jpg', 'cropped': True, 'score': 0, 'selectedForDisp': False}, 
                {'name': '937_right.jpg', 'cropped': True, 'score': 0, 'selectedForDisp': False}]
    imageSetPath = 'images_store/b958c466-1a15-4302-a201-be3b6f64c711_Session_Images/cropped_images'
    sessionInfo = evaluation(imageSetPath, sessionInfo)
    print(sessionInfo)

    # ['Corolla GR.jpg', '937_left.jpg', '937_right.jpg']
    

def test():
    modelPath = 'models/mobilenetv3_94.pth'
    # modelPath = 'models/resnet50_87.pth'
    state_dict = torch.load(modelPath, map_location=torch.device("cpu"))
    print(state_dict.keys())
    print(state_dict['model_state_dict'].keys())

if __name__ == '__main__':
    main()
    #test()
'''