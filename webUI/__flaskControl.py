from flask import Flask as _flask, request as _request, render_template as _render_template, jsonify as _jsonify
from typing import Optional as _Optional, Union as _Union, List as _List, Dict as _Dict, Any as _Any, Callable as _Callable, Tuple as _Tuple
from enum import Enum as _Enum


class ResponseType(_Enum):
    RENDER = 'render'
    JSON = 'json'
    NONE = 'none'


_CallBackFunctionType = _Callable[[_Dict[str, _Any]],
                                    _Tuple[ResponseType, _Dict[str, _Any]]]


def _callBackPlaceHolder(
        json: _Dict[str, _Any]) -> _Tuple[ResponseType, _Dict[str, _Any]]:
    return ResponseType.JSON, {
        "status": "error",
        "error-reason": "Not implemented"
    }


def exampleCallback(
        json: _Dict[str, _Any]) -> _Tuple[ResponseType, _Dict[str, _Any]]:
    if _callBackPlaceHolder is not None:
        raise NotImplementedError("The example function shouldn't be used.")
    elif _callBackPlaceHolder is not None:  # if this is a rendering function
        return ResponseType.RENDER, {"url": "index.html"}
    elif _callBackPlaceHolder is not None:  # if this is a json function
        return ResponseType.JSON, {
            "json key 1": "json value 1",
            "json key 2": "json value 2"
        }
    else:
        return ResponseType.NONE, {}
        


class App():

    def __init__(self,
                 name: _Optional[str] = None,
                 template_folder: _Optional[str] = None,
                 static_folder: _Optional[str] = None,
                 static_url_path: _Optional[str] = None,
                 root_path: _Optional[str] = None):
        self.__app = _flask(name if name is not None else __name__,
                             template_folder=template_folder,
                             static_folder=static_folder,
                             static_url_path=static_url_path,
                             root_path=root_path)
        self.__app.config['SECRET_KEY']

        self.__indexCallback: _CallBackFunctionType = _callBackPlaceHolder
        self.__callbackList: _Dict[str, _CallBackFunctionType] = {}

        @self.__app.route('/', methods=['GET', 'POST'])
        def index():
            if _request.args.get('keyWord') is None:
                indexResponse = self.__indexCallback(_request.args)
                if indexResponse[0] == ResponseType.RENDER:
                    return _render_template(indexResponse[1]["url"])
                else:
                    return

            response: _Dict[str, _Tuple[ResponseType, _Dict[str,
                                                               _Any]]] = {}
            for keyWord, callback in self.__callbackList.items():
                if keyWord in _request.args:
                    response[keyWord] = callback(_request.args)
            hasRender: bool = False
            hasJson: bool = False
            renderCount = 0
            for keyWord, value in response.items():
                if value[0] == ResponseType.RENDER:
                    hasRender = True
                    renderCount += 1
                elif value[0] == ResponseType.JSON:
                    hasJson = True
            if hasRender and hasJson:
                self.__app.logger.error(
                    "Render and json at the same time. List: %s",
                    response.keys())
                return _jsonify({
                    "status":
                    "error",
                    "error-reason":
                    "Render and json at the same time. List: {}".format(
                        response.keys())
                })
            if hasRender:
                if renderCount > 1:
                    self.__app.logger.error("Multiple render. List: %s",
                                            response.keys())
                    return _jsonify({
                        "status":
                        "error",
                        "error-reason":
                        "Multiple render. List: {}".format(response.keys())
                    })
                for keyWord in response:
                    if response[keyWord][0] == ResponseType.RENDER:
                        return _render_template(response[keyWord][1]["url"])
            elif hasJson:
                jsonResponse: _Dict[str, _Any] = {}
                for keyWord, value in response.items():
                    if value[0] == ResponseType.JSON:
                        jsonResponse[keyWord] = value[1]
                jsonResponse["status"] = "ok"
                return _jsonify(response)
            else:
                return _jsonify({"status": "ok"})

    def setIndexCallback(self, callback: _CallBackFunctionType) -> None:
        self.__indexCallback = callback

    def addCallback(self, keyWord: str,
                    callback: _CallBackFunctionType) -> bool:
        if keyWord in self.__callbackList:
            return False
        self.__callbackList[keyWord] = callback
        return True

    def run(self, port: int = 10000, debug: bool = False) -> int:
        try: 
            self.__app.run(port=port, debug=debug)
        except SystemExit:
            return 3
        except KeyboardInterrupt:
            return 0
        except:
            return 1
        return 0