/**
 * @fileoverview gRPC-Web generated client stub for isard
 * @enhanceable
 * @public
 */

// GENERATED CODE -- DO NOT EDIT!



const grpc = {};
grpc.web = require('grpc-web');


var google_api_annotations_pb = require('@/proto/third_party/google/api/annotations_pb.js')

var protoc$gen$swagger_options_annotations_pb = require('@/proto/third_party/protoc-gen-swagger/options/annotations_pb.js')
const proto = {};
proto.isard = require('./isard_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.isard.IsardClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

  /**
   * @private @const {?Object} The credentials to be used to connect
   *    to the server
   */
  this.credentials_ = credentials;

  /**
   * @private @const {?Object} Options for the client
   */
  this.options_ = options;
};


/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.isard.IsardPromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!proto.isard.IsardClient} The delegate callback based client
   */
  this.delegateClient_ = new proto.isard.IsardClient(
      hostname, credentials, options);

};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.isard.LoginLocalRequest,
 *   !proto.isard.LoginLocalResponse>}
 */
const methodInfo_Isard_LoginLocal = new grpc.web.AbstractClientBase.MethodInfo(
  proto.isard.LoginLocalResponse,
  /** @param {!proto.isard.LoginLocalRequest} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.isard.LoginLocalResponse.deserializeBinary
);


/**
 * @param {!proto.isard.LoginLocalRequest} request The
 *     request proto
 * @param {!Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.isard.LoginLocalResponse)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.isard.LoginLocalResponse>|undefined}
 *     The XHR Node Readable Stream
 */
proto.isard.IsardClient.prototype.loginLocal =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/isard.Isard/LoginLocal',
      request,
      metadata,
      methodInfo_Isard_LoginLocal,
      callback);
};


/**
 * @param {!proto.isard.LoginLocalRequest} request The
 *     request proto
 * @param {!Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.isard.LoginLocalResponse>}
 *     The XHR Node Readable Stream
 */
proto.isard.IsardPromiseClient.prototype.loginLocal =
    function(request, metadata) {
  return new Promise((resolve, reject) => {
    this.delegateClient_.loginLocal(
      request, metadata, (error, response) => {
        error ? reject(error) : resolve(response);
      });
  });
};


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.isard.UserDesktopsGetRequest,
 *   !proto.isard.UserDesktopsGetResponse>}
 */
const methodInfo_Isard_UserDesktopsGet = new grpc.web.AbstractClientBase.MethodInfo(
  proto.isard.UserDesktopsGetResponse,
  /** @param {!proto.isard.UserDesktopsGetRequest} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.isard.UserDesktopsGetResponse.deserializeBinary
);


/**
 * @param {!proto.isard.UserDesktopsGetRequest} request The
 *     request proto
 * @param {!Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.isard.UserDesktopsGetResponse)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.isard.UserDesktopsGetResponse>|undefined}
 *     The XHR Node Readable Stream
 */
proto.isard.IsardClient.prototype.userDesktopsGet =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/isard.Isard/UserDesktopsGet',
      request,
      metadata,
      methodInfo_Isard_UserDesktopsGet,
      callback);
};


/**
 * @param {!proto.isard.UserDesktopsGetRequest} request The
 *     request proto
 * @param {!Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.isard.UserDesktopsGetResponse>}
 *     The XHR Node Readable Stream
 */
proto.isard.IsardPromiseClient.prototype.userDesktopsGet =
    function(request, metadata) {
  return new Promise((resolve, reject) => {
    this.delegateClient_.userDesktopsGet(
      request, metadata, (error, response) => {
        error ? reject(error) : resolve(response);
      });
  });
};

export default proto.isard

