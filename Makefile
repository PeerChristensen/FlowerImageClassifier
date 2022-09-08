
create_env: 
	conda env create -f environment.yml

activate_env:
	conda activate flower_env

update_env:
	conda env update --prefix ./env --file environment.yml  --prune

start_env: create_env activate_env

run_script:
	python src/flower_image_scraper.py

clean_up:
	python src/clean_folders.py


	


	