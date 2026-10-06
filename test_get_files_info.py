from functions.get_files_info import get_files_info

print("Test 1:")
print(get_files_info("calculator","."))

print("\nTest 2:")
print(get_files_info("calculator","pkg"))

print("\nTest3:")
print(get_files_info("calculator","/bin"))

print("\nTest4:")
print(get_files_info("calculator","../"))
