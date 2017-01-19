% rebase('templates/layout.tpl', title='Login')

<form method="get" action="/login">
<div class="">
    <table style="max-width:200px; margin:0 auto">
        <tr>
            <td>
                <div class="form-group">
                    <label>Username</label>
                    <input name="username" class="form-control"/>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <input type="submit" value="Login" class="btn btn-primary"/>
            </td>
        </tr>
    </table>
</div>