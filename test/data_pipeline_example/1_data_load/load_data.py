import pandas as pd
import argparse


if __name__ == "__main__":
    
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        '--data_path',default='./Iris.csv', type=str,
        help="Input data path"
    )

    args = argument_parser.parse_args()
    data = pd.read_csv(args.data_path)
    print(data.shape)

    print("load data")

    data.to_csv('/result.csv', index=False)
    