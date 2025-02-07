def get_all_applets(self, request: Request) -> Response:
    """
    Get all applets
    """
    title = "Get all applets"
    token = self.runtime_data_initialised.boilerplate_incoming_initialised.get_token_if_present(
        request
    )
    if not token:
        return self.runtime_data_initialised.boilerplate_responses_initialised.bad_request(
            title
        )
    if self.runtime_data_initialised.boilerplate_non_http_initialised.is_token_correct(
        token
    ) is False:
        return self.runtime_data_initialised.boilerplate_responses_initialised.invalid_token(
            title
        )
    self.disp.log_debug(f"Token = {token}", title)
    applets_data = self.runtime_data_initialised.database_link.get_data_from_table(
        CONST.TAB_ACTIONS,
        "*"
    )
    if not applets_data or isinstance(applets_data, int):
        body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
            title=title,
            message="Applets not found.",
            resp="not found",
            token=token,
            error=True
        )
        return HCI.not_found(
            content=body,
            content_type=CONST.CONTENT_TYPE,
            headers=self.runtime_data_initialised.json_header
        )
    self.disp.log_debug(f"Applet found: {applets_data}", title)
    body = self.runtime_data_initialised.boilerplate_responses_initialised.build_response_body(
        title=title,
        message=applets_data,
        resp="success",
        token=token
    )
    return HCI.success(
        content=body,
        content_type=CONST.CONTENT_TYPE,
        headers=self.runtime_data_initialised.json_header
    )
