"""
@author: Vincent Bonnet
@description : Python code to export bone and point data into a dataset folder
"""
from .. import common
import hou_utils
import hou

def export_data_from_current_frame(sop_name):
    # Get the dataset directory (create directory if doesn't exist)
    common.get_dataset_dir()

    # Check the frame is in a valid range
    num_frames = hou.evalParm(sop_name+'/nFrames')
    frame_id = hou.intFrame()
    if frame_id > num_frames or frame_id <= 0:
        print('do not write frame_id({}) because > max_frames({})'.format(frame_id, num_frames))
        return

    # Export skeleton data
    # The skeleton hierarchy is frame invariant => only write it once
    skeleton_data = hou_utils.get_skeleton_data(sop_name)
    skeleton_data.save(overwrite=False)

    # Export skinning data
    # The skinning data is frame invariant => only write it once
    skinning_data = hou_utils.get_skinning_data(hou_utils.SMOOTH_SKINNING_INPUT_ID)
    skinning_data.save(overwrite=False)

    # Export clip data
    clip_data = hou_utils.get_clip_data(sop_name, skeleton_data, frame_id, num_frames)
    clip_data.save()

    # Console message
    clip_path = clip_data.get_clip_path(predicted=False)
    print('writing frame {}/{} from animation into the file : {}'.format(frame_id, num_frames, clip_path))
