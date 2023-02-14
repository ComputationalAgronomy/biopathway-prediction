import os


def generate_testset(enzyme_id, identity_param, copy_number_param):
    os.makedirs("test_model", exist_ok=True)
    for copy_number in range(1, copy_number_param + 1, 1):
        for identity in range(40, identity_param + 1, 1):
            with open(f"./test_model/copy_{copy_number}_identity_{identity}.csv", "w") as f:
                title = f"enzyme_id,identity\n"
                f.writelines(title)
                for id in range(3, 6):
                    to_write = f"{id},{identity}\n"
                    for iter in range(0, copy_number):
                        f.writelines(to_write)



generate_testset(1, 80, 3)
