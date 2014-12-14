var HideableWidget = function() {
    Widget.call(this);
};
inherits(HideableWidget, Widget);

HideableWidget.prototype.setState = function(state) {
    this._state = state;
    if (this._element) {
        if (state === 'shown') {
            this._element.show();
        } else if (state === 'hidden') {
            this._element.hide();
        }
    }
};

HideableWidget.prototype.onAfterShow = function() {};

HideableWidget.prototype.show = function() {
    this.setState('shown');
    this.onAfterShow();
};

HideableWidget.prototype.hide = function() {
    this.setState('hidden');
};

HideableWidget.prototype.decorate = function(element) {
    this._element = element;
};

/**
 * @constructor
 * The editor allows to type in message
 * and possibly recipients (if _editorType is 'new-thread')
 * supports editing new thread and reply
 */
var MessageComposer = function() {
    HideableWidget.call(this);
    this._editorType = undefined;//'new-thread', 'reply'
};
inherits(MessageComposer, WrappedElement);

MessageComposer.prototype.setMessageCenter = function(ctr) {
    this._messageCenter = ctr;
};

MessageComposer.prototype.setEditorType = function(type) {
    this._editorType = type;
};

MessageComposer.prototype.show = function() {
    this._textarea.show();
    this._textareaLabel.show();
    if (this._editorType === 'new-thread') {
        this._toInput.show();
        this._toInputLabel.show();
        this._cancelBtn.show();
        this._sendBtn.val(this._createThreadBtnText);
        var toInput = this._toInput;
        this._element.fadeIn('fast', function() {
            toInput.focus();
        });
    } else if (this._editorType === 'reply') {
        this._toInput.hide();
        this._toInputLabel.hide();
        this._cancelBtn.hide();
        this._sendBtn.val(this._replyBtnText);
        this._element.show();
        this._textarea.focus();
    }
};

MessageComposer.prototype.hide = function() {
    this._element.hide();
};

MessageComposer.prototype.cancel = function() {
    this._textarea.val('');
    this._textareaLabel.html('');
    this._toInput.val('');
    this._toInputLabel.html('');
    if (this._editorType == 'new-thread') {
        this.hide();
    }
};

MessageComposer.prototype.getSubmitData = function() {
    var data = {'text': this._textarea.val()};
    if (this._editorType === 'reply') {
        var thread = this._messageCenter.getThread();
        data['parent_id'] = thread.getId();
    } else if (this._editorType === 'new-thread') {
        data['to_usernames'] = this._toInput.val();
    }
    return data;
};

MessageComposer.prototype.dataIsValid = function() {
    var text = $.trim(this._textarea.val());
    var result = true;
    if (text === '') {
        this._textareaLabel.html(gettext('required'));
        result = false;
    }
    if (this._editorType === 'new-thread') {
        var to = $.trim(this._toInput.val());
        if (to === '') {
            this._toInputLabel.html(gettext('required'));
            result = false;
        }
    }
    return result;
};

/** override these two 
 * @param {object} data - the response data
 * these functions will run after .send() receives
 * the response
 */
MessageComposer.prototype.onSendSuccess = function(data) {
    var ctr = this._messageCenter;
    if (this._editorType === 'new-thread') {
        var count = ctr.getThreadList().getThreadsCount();
        if (count === 0) {
            ctr.loadThreadsForSender(-1);
            this.cancel();
        }
    } else if (this._editorType === 'reply') {
        var message = new Message();
        message.decorate($(data['html']));
        var thread = ctr.getThread();
        thread.addMessage(message);
        this._textarea.val('');
        this._textarea.focus();
    }
    notify.show(gettext('message sent'), true);
}


MessageComposer.prototype.onSendError = function(data) {
    if (this._editorType === 'reply') {
        return;
    }
    var missingUsers = data['missing_users']
    var errors = [];
    if (missingUsers) {
        var errorTpl = ngettext(
                            'user {{str}} does not exist',
                            'users {{str}} do not exist',
                            missingUsers.length
                        )
        errors.push(errorTpl.replace('{{str}}', joinAsPhrase(missingUsers)));
    }
    if (data['self_message']) {
        errors.push(gettext('cannot send message to yourself'));
    }
    this._toInputLabel.html(errors.join(', '));
};

MessageComposer.prototype.getSendUrl = function () {
    if (this._editorType == 'new-thread') {
        return this._createThreadUrl;
    } else if (this._editorType === 'reply') {
        return this._replyUrl;
    }
};

MessageComposer.prototype.send = function() {
    var me = this;
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: this.getSendUrl(),
        data: this.getSubmitData(),
        cache: false,
        success: function(data) {
            if (data['success']) {
                me.onSendSuccess(data);
            } else {
                me.onSendError(data);
            }
        }
    });
};

MessageComposer.prototype.decorate = function(element) {
    this._element = element;

    //textarea
    var textarea = element.find('textarea');
    this._textarea = textarea;
    var inputId = textarea.attr('id');

    //error label
    this._textareaLabel = element.find('label[for="' + inputId + '"]');

    var toInput = element.find('input[name="recipients"]');
    this._toInput = toInput;

    var userSelectHandler = function() {};

    var usersAc = new AutoCompleter({
        url: '/get-users-info/',//askbot['urls']['get_users_info'],
        minChars: 1,
        useCache: true,
        matchInside: true,
        maxCacheLength: 100,
        delay: 10,
        onItemSelect: userSelectHandler
    });
    usersAc.decorate(toInput);

    var label = element.find('label[for="' + toInput.attr('id') + '"]');
    this._toInputLabel = label;

    this._createThreadUrl = element.data('createThreadUrl');
    this._replyUrl = element.data('replyUrl');

    //cancel button
    var me = this;
    var cancelBtn = element.find('.js-cancel-btn');
    this._cancelBtn = cancelBtn;
    var cancelHandler = function() { me.cancel(); };
    setupButtonEventHandlers(cancelBtn, function() { me.cancel(); })

    //send button
    var me = this;
    var sendHandler = function() {
                            if (me.dataIsValid()){
                                me.send();
                            }
                        }
    var sendBtn = element.find('.js-send-btn');
    this._sendBtn = sendBtn;
    setupButtonEventHandlers(sendBtn, sendHandler);
    this._createThreadBtnText = element.data('createThreadBtnText');
    this._replyBtnText = element.data('replyBtnText');

    this.setEditorType(element.data('editorType'));
};

var ThreadHeading = function() {
    SimpleControl.call(this);
};
inherits(ThreadHeading, SimpleControl);

ThreadHeading.prototype.setParent = function(elem) {
    this._threadList = elem;
};

ThreadHeading.prototype.getParent = function() {
    return this._threadList;
};

ThreadHeading.prototype.getId = function() {
    return this._id;
};

ThreadHeading.prototype.decorate = function(element) {
    this._element = element;
    this._id = element.data('threadId');
    var deleter = element.find('.delete-or-restore');
    var me = this;
    setupButtonEventHandlers($(deleter), function() {
        me.getParent().deleteOrRestoreThread(me.getId());
        return false;
    });
};

/**
 * @constructor
 */
var ThreadList = function() {
    WrappedElement.call(this);
};
inherits(ThreadList, WrappedElement);

ThreadList.prototype.setMessageCenter = function(ctr) {
    this._messageCenter = ctr;
};

ThreadList.prototype.getOpenThreadHandler = function(threadId) {
    var messageCenter = this._messageCenter;
    return function() {
        messageCenter.openThread(threadId);
    };
};

ThreadList.prototype.deleteOrRestoreThread = function(threadId) {
    var ctr = this._messageCenter;
    ctr.deleteOrRestoreThread(threadId, this._senderId);
};

ThreadList.prototype.getThreadsCount = function() {
    if (self._threads) {
        return self._threads.length;
    } else {
        return 0;
    }
};

ThreadList.prototype.decorate = function(element) {
    if (!element || element.length === 0) {
        return;
    }
    this._element = element;
    var headingElements = element.find('.js-thread-heading');
    var me = this;
    var threads = [];
    $.each(headingElements, function(idx, headingElement) {
        var heading = new ThreadHeading();
        heading.setParent(me);
        heading.decorate($(headingElement));
        var threadId = heading.getId();
        heading.setHandler(me.getOpenThreadHandler(threadId));
        threads.push(heading);
    });
    this._threads = threads;
    this._emptyMemo = element.find('.js-no-threads');
    this._senderId = element.data('senderId');
}

/**
 * @constructor
 */
var Message = function() {
    Widget.call(this);
};
inherits(Message, Widget);

Message.prototype.getId = function() {
    return this._id;
};

Message.prototype.decorate = function(element) {
    this._element = element;
    this._id = element.data('messageId');
    element.find('abbr.timeago').timeago();
};


/**
 * @constructor
 */
var Thread = function() {
    WrappedElement.call(this);
};
inherits(Thread, WrappedElement);

Thread.prototype.getId = function() {
    return this._id;
};

Thread.prototype.getLastMessageId = function() {
    return this._messages.slice(-1)[0].getId();
};

Thread.prototype.dispose = function() {
    if (this._messages) {
        $.each(this._messages, function(idx, message) {
            message.dispose()
        });
    }
    Thread.superClass_.dispose.call(this);
};

Thread.prototype.addMessage = function(message) {
    var msgElement = message.getElement();
    if (this._ordering === 'reverse') {
        this._element.prepend(msgElement);
    } else if (this._ordering === 'forward') {
        this._element.append(msgElement);
    } else {
        throw 'Set data-thread-ordering either "forward" or "reverse"';
    }
};

Thread.prototype.decorate = function(element) {
    if (!element || element.length === 0) {
        return;
    }
    this._element = element;
    var messages = [];
    $.each(element.find('.js-message'), function(idx, item) {
        var message = new Message();
        message.decorate($(item));
        messages.push(message);
    });
    this._messages = messages;
    this._id = element.data('threadId');
    this._ordering = element.data('threadOrdering');
    element.find('abbr.timeago').timeago();
};


/**
 * @constructor
 * sender is a button which loads corresponding
 * list of threads (includes senders such as):
 * owner of inbox (sent messages)
 * all other users (incoming messages)
 * sent by specific users
 */
var Sender = function() {
    SimpleControl.call(this);
};
inherits(Sender, SimpleControl);

Sender.prototype.getId = function() {
    return this._id;
};

Sender.prototype.select = function() {
    this._element.addClass('selected');
};

Sender.prototype.unselect = function() {
    this._element.removeClass('selected');
};

Sender.prototype.decorate = function(element) {
    Sender.superClass_.decorate.call(this, element);
    this._id = element.data('senderId');
};


/**
 * @constructor
 * list of senders in the first column of inbox
 */
var SendersList = function() {
    WrappedElement.call(this);
    this._messageCenter = undefined;
};
inherits(SendersList, WrappedElement);

SendersList.prototype.setMessageCenter = function(ctr) {
    this._messageCenter = ctr;
};

SendersList.prototype.getSenders = function() {
    return this._senders;
};

SendersList.prototype.getSenderSelectHandler = function(sender) {
    var messageCenter = this._messageCenter;
    var me = this;
    return function() {
        $.map(me.getSenders(), function(s){ s.unselect() });
        sender.select();
        messageCenter.loadThreadsForSender(sender.getId());
    };
};

SendersList.prototype.decorate = function(element) {
    this._element = element;
    var senders = [];
    $.each(element.find('a'), function(idx, item) {
        var sender = new Sender();
        sender.decorate($(item));
        senders.push(sender);
    });

    this._senders = senders;

    var me = this;
    $.each(senders, function(idx, sender) {
        sender.setHandler(me.getSenderSelectHandler(sender));
    });
};


/**
 * @contsructor
 */
var MessageCenter = function() {
    Widget.call(this);
    this._loadingStatus = false;//true when loading in is process
};
inherits(MessageCenter, Widget);

MessageCenter.prototype.setState = function(state) {
    if (state === 'compose') {
        this._editor.show();
        this._threadListBox.hide();
        this._threadDetailsBox.hide();
    } else if (state === 'show-list') {
        this._editor.setEditorType('new-thread');
        this._editor.hide();
        this._threadListBox.show();
        this._threadDetailsBox.hide();
    } else if (state === 'show-thread') {
        this._threadListBox.hide();
        this._threadDetailsBox.show();
        this._editor.setEditorType('reply');
        this._editor.show();
    }
};

MessageCenter.prototype.openThread = function(threadId) {
    var url = this._urls['getThreads'] + threadId + '/';
    var me = this;
    var thread = this._thread;
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: url,
        cache: false,
        success: function(data) {
            if (data['success']) {
                me.clearThread();
                var thread = new Thread();
                thread.decorate($(data['html']));
                me.setThread(thread);
                me.setState('show-thread');
            }
        }
    });
};

MessageCenter.prototype.setThreadList = function(list) {
    this._threadList = list;
    this._threadListBox.append(list.getElement());
};

MessageCenter.prototype.clearThreadList = function() {
    if (this._threadList) {
        this._threadList.dispose();
    }
};

MessageCenter.prototype.getThreadList = function() {
    return this._threadList;
};

MessageCenter.prototype.setThread = function(thread) {
    this._thread = thread;
    this._threadDetailsBox.append(thread.getElement());
};

MessageCenter.prototype.getThread = function() {
    return this._thread;
};

MessageCenter.prototype.clearThread = function() {
    if (this._thread) {
        this._thread.dispose();
    }
};

MessageCenter.prototype.setLoadingStatus = function(loadingStatus) {
    this._loadingStatus = loadingStatus;
};

MessageCenter.prototype.hitThreadList = function(url, senderId, requestMethod) {
    if (this._loadingStatus === true) {
        return;
    };
    var me = this;
    $.ajax({
        type: requestMethod,
        dataType: 'json',
        url: url,
        cache: false,
        data: {sender_id: senderId},
        success: function(data) {
            if (data['success']) {
                me.clearThreadList();
                var threads = new ThreadList();
                threads.setMessageCenter(me);
                threads.decorate($(data['html']));
                me.setThreadList(threads);
                me.setState('show-list');
                me.setLoadingStatus(false);
            }
        },
        error: function() {
            me.setLoadingStatus(false);
        }
    });
    this.setLoadingStatus(true);
};

MessageCenter.prototype.deleteOrRestoreThread = function(threadId, senderId) {
    var url = this._urls['getThreads'] + threadId + '/delete-or-restore/';
    this.hitThreadList(url, senderId, 'POST');
};

MessageCenter.prototype.loadThreadsForSender = function(senderId) {
    var url = this._urls['getThreads'];
    this.hitThreadList(url, senderId, 'GET');
};

MessageCenter.prototype.decorate = function(element) {
    this._element = element;
    this._navBox = element.find('.pm-nav');
    this._mainBox = element.find('.pm-main');
    this._editorBox = element.find('.pm-editor');

    this._urls = {
        getThreads: element.data('getThreadsUrl'),
        getThreadDetails: element.data('getThreadDetailsUrl'),
        reply: element.data('replyUrl')
    };

    //set up PM inbox navigaion, inaptly called SendersList
    var nav = new SendersList();
    nav.setMessageCenter(this);
    nav.decorate(this._navBox);
    this._navigation = nav;

    var listBox = element.find('.js-thread-list-container');
    this._threadListBox = listBox;

    //read message list
    var threads = new ThreadList();
    threads.setMessageCenter(this);
    this._threadList = threads;
    threads.decorate(listBox.find('.js-thread-list'));

    var detailsBox = element.find('.js-thread-details-container');
    this._threadDetailsBox = detailsBox;

    //add empty thread container or decorate existing one
    var thread = new Thread();
    this._thread = thread;
    thread.decorate(element.find('.js-thread'));

    //create editor
    var editor = new MessageComposer();
    editor.decorate($('.pm-editor'));
    editor.setMessageCenter(this);
    this._editor = editor;

    //activate compose button
    var btn = element.find('.js-compose-btn');
    var me = this;
    setupButtonEventHandlers(btn, function(){ 
        editor.setEditorType('new-thread');
        me.setState('compose') 
    });
    this._composeBtn = btn;
};

var msgCtr = new MessageCenter();
msgCtr.decorate($('.group-messaging'));
