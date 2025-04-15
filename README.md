# 🎯 OpenCV를 이용한 AR 카메라 자세 추정

이 프로젝트는 체스보드 패턴을 이용해 카메라의 자세(pose)를 추정하고,  
영상 위에 3D AR 오브젝트(큐브)를 실시간으로 렌더링하는 프로그램입니다.

---

## 📌 주요 기능

- `solvePnP()`를 활용한 카메라 자세 추정
- 체스보드 위에 3D 큐브를 실시간으로 렌더링
- 결과 이미지 및 영상 저장
- Python + OpenCV 기반 구현

---

## 📷 결과 이미지

AR 큐브가 체스보드 위에 표시된 예시 프레임입니다:

![AR Pose Result](ar_pose_result.png)

---

## 🎥 결과 영상

체스보드를 움직이면, AR 큐브가 따라오는 모습을 확인할 수 있습니다:

[▶️ demo_ar_pose.mp4](demo_ar_pose.mp4)

---

## 🛠️ 실행 방법

1. 저장소를 클론합니다
2. 필요한 라이브러리를 설치합니다:
   ```bash
   pip install opencv-python numpy
