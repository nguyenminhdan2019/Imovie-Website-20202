# Imovie - Website GR 20202 - HUST
Website sử dụng **Django** là backend framework, sử dụng hệ quản trị CSDL SQLite3, có thể chạy trên Docker 

Trong version hiện tại, Các chức năng sau đã được triển khai:
- **Search Engine** Sử dụng Inverted Index, LRU Cache 
- Quản lý thành viên 
- Quản lý phim
- User (Login, Register, Active by Mail ,Forgot password)
- User Profile (Wall, Edit Profile)
- User Social ( Follow, Newfeed, Post, Reply, Like, Report, Notification)
- Review Movie (Review, Rate, Reply review, Tagging movie)
- Realtime function (Websocket, Ajax)
- Login via Facebook (**OAuth** with Facebook API)
- **Recommender** 

***

## Index of Contents
1. [Data and Database](#data-and-database)
2. [Search Engine and Cache](#search-engine)
3. [Recommender](#recommender)
4. [Demo](#demo)

<a name="data-and-database"></a>

## Data and Database 
Có hơn 5000 thông tin bộ phim được public tại [movie dataset](https://www.kaggle.com/oxanozaep/imdb-eda/data). Tôi đã sử dụng thư viện [imdbpie](https://pypi.org/project/imdbpie/) để lấy và xử lý chúng.Hiện tại tôi đang sử dụng hơn **1000phim** trong database. 

<a name="search-engine"></a>

## Search Engine and Cache

- **Search Index**: Xây dựng cấu trúc chỉ mục ngược để cho phép tìm kiếm toàn văn nhanh, tiện lợi
- **Rank**: Các kết quả tìm kiếm được sắp xếp, phim sắp xếp theo lượt đánh giá, diễn viên theo tổng số phim tham gia
- **Cache**: Dùng Cache để lưu lại các kết quả tìm kiếm , giúp tìm kiếm nhanh hơn. Sử dụng LRU Cache để loại bỏ các tìm kiếm ít được sử dụng.

<a name="recommender"></a>

## Recommender

**Content Based**

Sử dụng **Content Based** để gợi ý các phim dựa theo lịch sử yêu thích của người dùng. Tôi sử dụng tập các tag được cồng đồng gắn vào phim từ dữ liệu [**Movielens 25m**](https://grouplens.org/datasets/movielens/25m/).

Tôi sử dụng **Jaccard Index** và **Cosine Similarity** để tính toán độ tương đồng của các tập các tag gắn vào phim. 

Trong trường hợp sử dụng ** Cosine Similarity ** tôi đã vector hoá các bộ phim bằng cách sử dụng **Doc2Vec** thông qua thư viện **Gensim**

**Collaborative Filtering**
Tôi sử dụng lọc cộng tác để gợi ý người dùng theo dõi những người khác. Bằng cách tìm K người dùng tương đồng nhất với người dùng cần giới thiệu, sau đó từ danh sách theo dõi của K người đó, gợi ý cho người dùng cần giới thiệu.

**Recommend Search**
Gợi ý tìm kiếm thông qua các phiên tìm kiếm của người dùng khác trong lịch sử, nếu tồn tại phiên tìm kiếm tương đồng và có kết quả, gợi ý cho người dùng.

<a name="demo"></a>

## Demo

Dưới đây là các link demo chi tiết các nhóm chức năng :
1. Nhóm chức năg Quản trị viên [Admin Site](https://www.youtube.com/watch?v=eV8ekPgnYhs)
2. Nhóm chức năng Thành viên [User](https://www.youtube.com/watch?v=iVZ4qBHkLj0)

