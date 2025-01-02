import torch
from PIL import Image
from glaucoma_model import GlaucomaDiagnoser
import torchvision.transforms as transforms

# modelPath = 'models/mobilenetv3_94.pth'
modelPath = 'models/resnet50_87.pth'

def evaluationModel(modelPath, ImagePath):
    image = Image.open(ImagePath).convert("RGB")
    #image = Image.open(ImagePath)

    model = GlaucomaDiagnoser()
    state_dict = torch.load(modelPath, map_location=torch.device("cpu"), weights_only=False)
    model_state_dict = state_dict["model_state_dict"]
    model.load_state_dict(model_state_dict, strict=False)

    model.eval()

    transform = transforms.ToTensor()

    # Convert the image to a PyTorch tensor
    input_tensor = transform(image)
    input_tensor = input_tensor.unsqueeze(0)
    
    outputs = model(input_tensor)
    _, predicted = torch.max(outputs.data, 1)
    return predicted.item()

def evaluation(cropImageLocation, sessionInfo):
    for imageInfo in sessionInfo:
        if imageInfo['cropped'] == True:
            prediction = evaluationModel(modelPath, f'{cropImageLocation}/cropped_{imageInfo['name']}')

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
    evaluation(imagePaths[2], ['Corolla GR.jpg', '937_left.jpg', '937_right.jpg'], 
               [{'name': 'Corolla GR.jpg', 'cropped': False, 'score': 0, 'selectedForDisp': False}, 
                {'name': '937_left.jpg', 'cropped': True, 'score': 0, 'selectedForDisp': False}, 
                {'name': '937_right.jpg', 'cropped': True, 'score': 0, 'selectedForDisp': False}])

def test():
    state_dict = torch.load(modelPath, map_location=torch.device("cpu"))
    print(state_dict.keys())
    print(state_dict['model_state_dict'].keys())

if __name__ == '__main__':
    main()
    #test()
'''