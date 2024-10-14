# import os 
# from PIL import Image

# from modules.tools import GetRootProject
# from modules.log import LOG
# from modules.log import LOG

# BASE_DIR = GetRootProject() + "\\dir"

# def create_thumbnail(image_path, thumb_path, size=(128, 128)):
#     with Image.open(image_path) as img:
#         img.thumbnail(size)
#         img.save(thumb_path)

# def scanforthumbnail(folder_path):
#     counter = 0
#     for root, dirs, files in os.walk(folder_path):
#         for file_name in files:
#             if "thumb_" not in file_name:
#                 if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
#                     # Define the path for the original image and its thumbnail
#                     image_path = os.path.join(root, file_name)
#                     thumb_path = os.path.join(root, os.path.splitext('thumb_' + file_name)[0] + os.path.splitext(file_name)[1])

#                     # Check if thumbnail already exists
#                     if not os.path.exists(thumb_path):
#                         print(f"Creating thumbnail for: {image_path}")
#                         create_thumbnail(image_path, thumb_path)
#                     else:
#                         print(f"Thumbnail already exists for: {image_path}")
#     LOG.info()
# # # Process the folder
# # scanforthumbnail(BASE_DIR)
