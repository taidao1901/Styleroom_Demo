activate:
	cd env && \
	source $(poetry env info --path)/bin/activate && \
	cd ..
run: 
	streamlit run main.py --server.port=8081 --server.address=0.0.0.0