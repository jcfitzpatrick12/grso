'''
script will convert the binary and header data to fits files in data folder
'''
from src.utils import Tags
import src.run_observations.batch.proc_batch as proc_batch

def main(tag_1, tag_2):
    proc_batch.main(tag_1)
    proc_batch.main(tag_2)

if __name__ == '__main__':
    tag_1, tag_2 = Tags.get_tags_from_args()
    #tag_1 will apply the parameters in config_dict to Tuner 1 of the the RSPDuo, similarly for tag_2
    main(tag_1, tag_2)