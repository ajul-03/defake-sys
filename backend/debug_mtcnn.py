
import traceback
try:
    print("Attempting to import mtcnn...")
    import mtcnn
    print(f"mtcnn version: {mtcnn.__version__}")
    from mtcnn import MTCNN
    print("MTCNN imported successfully!")
    detector = MTCNN()
    print("MTCNN detector initialized.")
except Exception as e:
    print("FAILED to import mtcnn.")
    traceback.print_exc()
