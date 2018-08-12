from django.shortcuts import render_to_response
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .settings import MEDIA_ROOT, ALLOWED_SUFFIX
import os
from datetime import datetime


@csrf_exempt
@require_GET
def index(request):
    return render_to_response('index.html')


@csrf_exempt
@require_POST
def tianmao_img(request):
    """
    接收前端发送的天猫（淘宝）营业执照图片（支持批量），加以处理并提取其中的所需信息，以excel表格的形式返回给前端
    :param request:
    :return:excel文件流
    """
    try:
        upload_dir = os.path.join(MEDIA_ROOT, 'uploads/')
        download_dir = os.path.join(MEDIA_ROOT, 'downloads/')
        for source in request.FILES.values():
            suffix = source.name.split('.')[-1]
            if suffix in ALLOWED_SUFFIX:
                file_path = upload_dir + datetime.now().strftime("%Y%m%d%H%M%S%f") + '.' + suffix
                with open(file_path, 'wb') as f:
                    if source.size != 0:
                        for block in source.chunks():
                            f.write(block)
        # 图像处理完成后将表格保存在/media/downloads目录下，并且返回excel文件
        filename = 're.xlsx'
        with open(download_dir + filename, encoding='utf-8') as f:
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="{0}"' \
                .format(datetime.now().strftime("%Y%m%d%H%M%S") + '.xlsx')
            response.write(f)
            return response

    except Exception as e:
        print(e)
        return JsonResponse({'status': 500})
