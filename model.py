import numpy as np
import torch
import torch.nn as nn


USE_CUDA = torch.cuda.is_available()
device = torch.device('cuda:0' if USE_CUDA else 'cpu')


class SalesPredictionNN(nn.Module):
    def __init__(self, cat_dim, n_cont, layers, out_sz, p=0.5):
        super().__init__()
        embedded_dim = [(i, min(50, (i + 1) // 2)) for i in cat_dim]
        self.embd_list = nn.ModuleList([nn.Embedding(inp, out) for inp, out in embedded_dim])
        self.drpout = nn.Dropout(p)
        self.batchnorm = nn.BatchNorm1d(n_cont)

        layerslist = []
        n_emb = sum([out for inp, out in embedded_dim])
        n_in = n_emb + n_cont

        for i in layers:
            layerslist.append(nn.Linear(n_in, i))
            layerslist.append(nn.ReLU(inplace=True))
            layerslist.append(nn.BatchNorm1d(i))
            layerslist.append(nn.Dropout(p))
            n_in = i
        layerslist.append(nn.Linear(layers[-1], out_sz))

        self.layers = nn.Sequential(*layerslist)

    def forward(self, x_cat, x_cont):
        embeddings = []
        for i, e in enumerate(self.embd_list):
            embeddings.append(e(x_cat[:, i]))
        x = torch.cat(embeddings, 1)
        x = self.drpout(x)

        x_cont = self.batchnorm(x_cont)

        x = torch.cat([x, x_cont], axis=1)

        x = self.layers(x)

        return x


def evaluation(gen_aggr_cl="일반", usage="제2종근린생활시설", sector="한식음식점", com_dist="전통시장", sub1=0, sub2=0, sch1=0, sch2=0, mart1=0, mart2=0):

    # Embedding
    gen_aggr_cl_dict = {'일반': 0, '집합': 1}
    usage_dict = {'제1종근린생활시설': 0, '제2종근린생활시설': 1, '판매시설': 2}
    sector_dict = {'PC방': 0, '가구': 1, '가방': 2, '가전제품': 3, '가전제품수리': 4, '고시원': 5, '골프연습장': 6, '네일숍': 7, '노래방': 8, '당구장': 9, '문구': 10,
     '미곡판매': 11, '미용실': 12, '반찬가게': 13, '부동산중개업': 14, '분식전문점': 15, '서적': 16, '섬유제품': 17, '세탁소': 18, '수산물판매': 19,
     '슈퍼마켓': 20,
     '스포츠 강습': 21, '스포츠클럽': 22, '시계및귀금속': 23, '신발': 24, '안경': 25, '애완동물': 26, '양식음식점': 27, '여관': 28, '예술학원': 29,
     '완구': 30,
     '외국어학원': 31, '운동/경기용품': 32, '육류판매': 33, '의료기기': 34, '의약품': 35, '인테리어': 36, '일반교습학원': 37, '일반의류': 38, '일반의원': 39,
     '일식음식점': 40, '자동차미용': 41, '자동차수리': 42, '자전거 및 기타운송장비': 43, '전자상거래업': 44, '제과점': 45, '조명용품': 46, '중식음식점': 47,
     '철물점': 48,
     '청과상': 49, '치과의원': 50, '치킨전문점': 51, '커피-음료': 52, '컴퓨터및주변장치판매': 53, '패스트푸드점': 54, '편의점': 55, '피부관리실': 56,
     '한식음식점': 57,
     '한의원': 58, '핸드폰': 59, '호프-간이주점': 60, '화장품': 61, '화초': 62}
    com_dist_dict = {'골목상권': 0, '발달상권': 1, '전통시장': 2}
    
    #임베딩 시킨 명목형 변수와 연속형 변수를 텐서화
    cat_features = np.array([gen_aggr_cl_dict[gen_aggr_cl], usage_dict[usage], sector_dict[sector],com_dist_dict[com_dist] ])
    cat_features = torch.tensor(cat_features.reshape(1,4), dtype = torch.int64)

    cont_features = np.array([sub1, sub2, sch1, sch2, mart1, mart2])
    cont_features = torch.tensor(cont_features.reshape(1,6), dtype= torch.float)
    
    #후 학습시킨 모델에 적용
    model1=SalesPredictionNN([2, 3, 63, 3],6,[100,50],1,p=0.4)
    model1.load_state_dict(torch.load('PriceWeights.pt'))
    model1.eval()

    #return (cat_features, cont_features)
    return  model1(cat_features, cont_features).item()
