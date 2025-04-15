import cv2
import numpy as np

# --- 체스보드 설정 ---
CHECKERBOARD = (6, 9)  # (행, 열) 내부 코너 개수
square_size = 0.024  # 1칸의 실제 크기 (단위: meter)

# --- 3D 좌표 설정 (z=0 평면 위의 체스보드 코너) ---
objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[1], 0:CHECKERBOARD[0]].T.reshape(-1, 2)
objp *= square_size

# --- AR 오브젝트 (큐브) 정의 ---
cube = np.float32([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
    [0, 0, -1], [1, 0, -1], [1, 1, -1], [0, 1, -1]
]) * square_size

# --- 캘리브레이션 결과 (직접 측정한 값으로 교체 필요) ---
camera_matrix = np.array([[800, 0, 320],
                          [0, 800, 240],
                          [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.zeros((5, 1))  # 왜곡 계수 (보정했다면 실제값 사용)

# --- 비디오 캡처 시작 ---
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if not ret:
    print("❌ 카메라 열기 실패")
    cap.release()
    exit()

# --- 영상 저장 세팅 ---
h, w = frame.shape[:2]
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('demo_ar_pose.mp4', fourcc, 20.0, (w, h))

# --- 이미지 저장 플래그 ---
saved = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret_cb, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret_cb:
        print("✅ 체스보드 인식 성공")
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                     criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))

        # 코너 시각화
        cv2.drawChessboardCorners(frame, CHECKERBOARD, corners2, ret_cb)

        # 카메라 자세 추정
        ret_pnp, rvecs, tvecs = cv2.solvePnP(objp, corners2, camera_matrix, dist_coeffs)

        # 큐브 투영
        imgpts, _ = cv2.projectPoints(cube, rvecs, tvecs, camera_matrix, dist_coeffs)
        imgpts = np.int32(imgpts).reshape(-1, 2)

        # 바닥 사각형
        frame = cv2.drawContours(frame, [imgpts[:4]], -1, (0, 255, 0), 4)
        # 옆면 연결선
        for i, j in zip(range(4), range(4, 8)):
            frame = cv2.line(frame, tuple(imgpts[i]), tuple(imgpts[j]), (255, 0, 0), 4)
        # 윗면 사각형
        frame = cv2.drawContours(frame, [imgpts[4:]], -1, (0, 0, 255), 4)

        # ✅ 이미지 저장 (1회만)
        if not saved:
            cv2.imwrite("ar_pose_result.png", frame)
            print("🖼️ 이미지 저장 완료: ar_pose_result.png")
            saved = True
    else:
        print("❌ 체스보드 인식 실패")

    # 영상 저장
    out.write(frame)

    # 실시간 출력
    cv2.imshow('Pose Estimation AR Cube', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료 처리
cap.release()
out.release()
cv2.destroyAllWindows()
print("✅ 영상 저장 완료: demo_ar_pose.mp4")
