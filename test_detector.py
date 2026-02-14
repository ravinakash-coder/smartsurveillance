from src.object_detector import ObjectDetector
import logging
logging.basicConfig(level=logging.INFO)
print('Creating detector...')
d = ObjectDetector()
print('model:', d.model)
print('has_fallback:', getattr(d, 'has_fallback', None))
try:
    print('fallback exists:', hasattr(d, 'fallback'))
except Exception as e:
    print('fallback access error', e)
