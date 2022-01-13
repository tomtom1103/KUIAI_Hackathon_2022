# Journey Lee: KUIAI Hackathon 2022🐯

##### Journey Lee is a collaborative effort for the 2022 KUIAI Hackathon for Korea University. It was made from scratch by Thomas and John Lee between the course of 72 Hours. Enjoy!🐯 

[Journey Lee Web App🚀](https://share.streamlit.io/tomtom1103/kuiai_hackathon_2022/main/JL_app.py)

***

### Developers🧑‍💻
**Thomas Lee🐱**
\
[Github](https://github.com/tomtom1103)
\
[Mail](tomtom1103@korea.ac.kr)

**John Lee‍🧑‍🚀**
\
[Github](https://github.com/johnbuzz98)
\
[Mail](johnbuzz98@korea.ac.kr)

***

### File Explanation
**data_upload/** is the collection of preprocessed .pkl files for the web app to function.
\
\
**data_upload_buzz/** is the collection of preprocessed .pkl files for the web app to function.
\
\
**JL_files.py** are the pure python web app streamlit files.

**main_engine.py** is the core PyTorch based engine that predicts the expected sales given a coordinate.

**PriceWeights.pt, SalesPrice.pt** are the trained weights for the main_engine.py to function.

**requirements.txt** is the req. file for the web app to function.

***

*Disclaimer:*
\
*Journey Lee will only function through the link and not function locally,
since it has been configured with personal API TOKENS
of the developers. If the user wishes to run the app locally, we advise
the user to issue Naver APIs, Mapbox APIs, and a Kakao API and add it to .streamlit/secrets.toml.*