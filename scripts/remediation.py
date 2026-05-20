import json

PACKAGE_FILE = "../app/package.json"

# Vulnerability data (for MVP hardcoded)
vulnerable_package = "body-parser"
fixed_version = "^1.20.3"

# Load package.json
with open(PACKAGE_FILE, "r") as f:
    package_data = json.load(f)

# Update dependency
if vulnerable_package in package_data["dependencies"]:
    old_version = package_data["dependencies"][vulnerable_package]

    package_data["dependencies"][vulnerable_package] = fixed_version

    print(f"\nUpdated {vulnerable_package}")
    print(f"Old Version: {old_version}")
    print(f"New Version: {fixed_version}")

# Save updated package.json
with open(PACKAGE_FILE, "w") as f:
    json.dump(package_data, f, indent=4)

print("\nRemediation completed successfully.")



DOCKERFILE = "../docker/Dockerfile"

old_base = "node:14"
new_base = "node:20-alpine"

with open(DOCKERFILE, "r") as f:
    docker_content = f.read()

docker_content = docker_content.replace(old_base, new_base)

with open(DOCKERFILE, "w") as f:
    f.write(docker_content)

print("\nDockerfile updated successfully.")